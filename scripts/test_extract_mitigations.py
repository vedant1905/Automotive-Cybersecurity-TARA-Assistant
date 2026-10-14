import asyncio
import re
import csv
import pypdfium2 as pdfium
import winocr

async def extract_all_mitigations():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    
    # We will parse Part B (pages 23-28) and Part C (pages 29-30)
    # Each row in the table connects Table A1 references (threat IDs) to a Mitigation (ID and text)
    
    mitigation_entries = []
    
    # Let's inspect pages 23 to 30
    for page_idx in range(22, 30):
        part = "B" if page_idx < 28 else "C"
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            if r.y < 250:
                continue
            lines.append({
                "x": r.x,
                "y": r.y,
                "text": l.text.strip()
            })
        lines.sort(key=lambda item: item["y"])
        
        # Threat references are around x=280..380
        # Threat refs match pattern like "6.1", "6.2", "1.1 & 3.1", "15.1, 15.2", "28.2", etc.
        t_ref_lines = []
        for l in lines:
            if 250 <= l["x"] <= 380:
                # check if contains digits and dots or &
                if re.search(r"\d+\.\d+", l["text"]) or re.match(r"^\d+$", l["text"]):
                    t_ref_lines.append(l)
                    
        for i, t_ref in enumerate(t_ref_lines):
            next_y = t_ref_lines[i+1]["y"] if i+1 < len(t_ref_lines) else 9999
            
            # Find mitigation ID (x around 880..990)
            m_id = ""
            for l in lines:
                if 870 <= l["x"] <= 990 and t_ref["y"] - 30 <= l["y"] < next_y:
                    txt = l["text"].replace("MIO", "M10").replace("Mll", "M11").replace("MI ", "M1").replace("M1 3", "M13")
                    if re.match(r"^M\d+", txt):
                        m_id = txt
                    elif re.match(r"^\d+$", txt) and int(txt) in [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]:
                        m_id = f"M{txt}"
                        
            # Find mitigation description (x >= 990)
            desc_lines = []
            for l in lines:
                if "Mitigation" in l["text"] and l["y"] < 350:
                    continue
                if l["x"] >= 990 and t_ref["y"] - 30 <= l["y"] < next_y:
                    desc_lines.append(l["text"])
                    
            desc = " ".join(desc_lines).strip()
            
            # If no explicit M-tag in cell, check if row inherits or generate logical ID
            if not m_id:
                # check if there was an M-tag on same line or nearby
                m_match = re.search(r"\bM\d+\b", desc)
                if m_match:
                    m_id = m_match.group(0)
                else:
                    m_id = f"PART_{part}_ROW_{len(mitigation_entries)+1}"
                    
            if desc:
                mitigation_entries.append({
                    "mitigation_id": m_id,
                    "description": desc,
                    "part": part,
                    "mapped_threat_ids": t_ref["text"]
                })
                
    print(f"Extracted {len(mitigation_entries)} mitigation rows:")
    for m in mitigation_entries[:15]:
        print(f"[{m['part']}] {m['mitigation_id']:10} | mapped: {m['mapped_threat_ids']:12} | {m['description'][:50]}...")
        
    return mitigation_entries

if __name__ == "__main__":
    asyncio.run(extract_all_mitigations())
