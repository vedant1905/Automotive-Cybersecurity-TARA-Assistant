import asyncio
import re
import csv
import pypdfium2 as pdfium
import winocr

async def parse_mitigations():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    
    mitigations = []
    
    # Part B: pages 23 to 28 (indices 22 to 27)
    for page_idx in range(22, 28):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            if r.y < 250:
                continue
            lines.append((r.x, r.y, l.text.strip()))
        lines.sort(key=lambda item: item[1])
        
        # Threat refs are in x=250..400
        # Threat text in x=420..880
        # Mitigation Ref (e.g. M1..M24) in x=880..980
        # Mitigation description in x>=980
        m_refs = []
        for x, y, text in lines:
            # Clean OCR common misreads for M-tags (e.g. MIO -> M10, MI 3 -> M13, M9, M14 -> M14)
            cleaned = text.replace("MIO", "M10").replace("MI ", "M1").replace("M1 3", "M13").replace("MO", "M0")
            if re.match(r"^M\d+$", cleaned):
                m_refs.append((y, cleaned))
            elif re.match(r"^\d+$", text) and int(text) in [14, 15, 23, 24] and 900 <= x <= 980:
                m_refs.append((y, f"M{text}"))
                
        print(f"Page {page_idx+1} (Part B): found {len(m_refs)} mitigations: {[m[1] for m in m_refs]}")

    # Part C: pages 29 to 30 (indices 28 to 29)
    for page_idx in range(28, 30):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            if r.y < 250:
                continue
            lines.append((r.x, r.y, l.text.strip()))
        lines.sort(key=lambda item: item[1])
        
        m_refs = []
        for x, y, text in lines:
            cleaned = text.replace("MIO", "M10").replace("MI ", "M1").replace("M1 3", "M13").replace("MO", "M0")
            if re.match(r"^M\d+$", cleaned):
                m_refs.append((y, cleaned))
            elif re.match(r"^\d+$", text) and int(text) in [14, 15, 23, 24] and 900 <= x <= 980:
                m_refs.append((y, f"M{text}"))
        print(f"Page {page_idx+1} (Part C): found {len(m_refs)} mitigations: {[m[1] for m in m_refs]}")

if __name__ == "__main__":
    asyncio.run(parse_mitigations())
