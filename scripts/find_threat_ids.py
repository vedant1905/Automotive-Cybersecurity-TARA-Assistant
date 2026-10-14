import asyncio
import re
import pypdfium2 as pdfium
import winocr

async def find_threat_ids():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    pages_to_process = range(16, 22)
    
    found_ids = []
    
    for page_idx in pages_to_process:
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        
        page_lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            # filter header
            min_y = 1900 if page_idx == 16 else 280
            if r.y < min_y:
                continue
            page_lines.append((r.x, r.y, l.text.strip()))
            
        # Threat IDs are in column around x=900..950
        for x, y, text in page_lines:
            if 870 <= x <= 960 and re.match(r"^\d+\.\d+$", text):
                found_ids.append((page_idx + 1, x, y, text))
                
    print(f"Total threat IDs found: {len(found_ids)}")
    for p, x, y, tid in found_ids:
        print(f"Page {p} (y={y:4.0f}): {tid}")

if __name__ == "__main__":
    asyncio.run(find_threat_ids())
