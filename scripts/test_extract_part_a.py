import asyncio
import re
import pypdfium2 as pdfium
import winocr

async def extract_part_a():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    
    # Part A spans pages 17 to 22 (0-indexed: 16 to 21)
    pages_to_process = range(16, 22)
    
    current_category = ""
    current_sub_cat_num = ""
    current_sub_cat_text = ""
    
    threats = []
    
    for page_idx in pages_to_process:
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        
        # Sort lines vertically by y-coordinate
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            lines.append({
                "text": l.text.strip(),
                "x": r.x,
                "y": r.y,
                "w": r.width,
                "h": r.height
            })
        lines.sort(key=lambda item: (item["y"], item["x"]))
        
        # Filter lines within table bounds
        table_lines = [l for l in lines if l["y"] > (1900 if page_idx == 16 else 280)]
        
        print(f"Page {page_idx+1}: {len(table_lines)} table lines")

if __name__ == "__main__":
    asyncio.run(extract_part_a())
