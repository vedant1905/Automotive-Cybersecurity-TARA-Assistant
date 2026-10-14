import asyncio
import re
import csv
import pypdfium2 as pdfium
import winocr

CATEGORIES = [
    ("4.3.1", "4.3.1 Threats regarding back-end servers related to vehicles in the field"),
    ("4.3.2", "4.3.2 Threats to vehicles regarding their communication channels"),
    ("4.3.3", "4.3.3 Threats to vehicles regarding their update process"),
    ("4.3.4", "4.3.4 Threats to vehicles regarding unintended human actions facilitating a cyber-attack"),
    ("4.3.5", "4.3.5 Threats to vehicles regarding their external connectivity and connections"),
    ("4.3.6", "4.3.6 Potential targets of, or motivations for, an attack on vehicles"),
    ("4.3.7", "4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened")
]

async def parse_part_a():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    # Part A spans pages 17 to 22 (0-indexed 16 to 21)
    
    all_threat_rows = []
    current_category = CATEGORIES[0][1]
    current_subcat = ""
    
    for page_idx in range(16, 22):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        
        min_y = 1900 if page_idx == 16 else 280
        
        # Collect lines with bounding box
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            if r.y < min_y:
                continue
            lines.append((r.x, r.y, l.text.strip()))
            
        # Find all threat IDs on this page
        # Threat IDs are around x=870..970 and match \d+\.\d+
        t_ids_on_page = []
        for x, y, text in lines:
            if 870 <= x <= 970 and re.match(r"^\d+\.\d+$", text):
                t_ids_on_page.append((y, text))
                
        t_ids_on_page.sort(key=lambda item: item[0])
        
        # For each threat ID, its description consists of lines in x >= 970
        # between this threat ID's y and the next threat ID's y (or page bottom)
        for i, (tid_y, tid) in enumerate(t_ids_on_page):
            next_y = t_ids_on_page[i+1][0] if i+1 < len(t_ids_on_page) else 9999
            
            # Category update if present above this threat ID
            for x, y, text in lines:
                if x < 450 and tid_y - 200 <= y <= tid_y + 100:
                    for prefix, full_cat in CATEGORIES:
                        if prefix in text:
                            current_category = full_cat
                            
            # Subcategory update
            subcat_lines = []
            for x, y, text in lines:
                if 520 <= x < 880 and tid_y - 40 <= y < next_y:
                    subcat_lines.append(text)
            if subcat_lines:
                current_subcat = " ".join(subcat_lines)
                
            # Threat description lines
            desc_lines = []
            for x, y, text in lines:
                # Header filter
                if "Example of vulnerability" in text:
                    continue
                if x >= 970 and tid_y - 30 <= y < next_y:
                    desc_lines.append(text)
                    
            desc = " ".join(desc_lines)
            all_threat_rows.append({
                "threat_id": tid,
                "category": current_category,
                "sub_category": current_subcat,
                "threat_description": desc
            })
            
    print(f"Total extracted Part A rows: {len(all_threat_rows)}")
    for r in all_threat_rows:
        print(f"[{r['threat_id']}] {r['category'][:25]}... | {r['sub_category'][:30]}... | {r['threat_description'][:50]}...")
        
    return all_threat_rows

if __name__ == "__main__":
    asyncio.run(parse_part_a())
