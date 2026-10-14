import asyncio
import pypdfium2 as pdfium
import winocr

async def scan_pages():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    print(f"Scanning pages 15 to {len(pdf)}...")
    for i in range(14, len(pdf)):
        img = pdf[i].render(scale=2).to_pil()
        res = await winocr.recognize_pil(img)
        header_lines = [l.text for l in res.lines if l.words and l.words[0].bounding_rect.y < 350]
        header_text = " | ".join(header_lines)
        print(f"Page {i+1}: {header_text[:120]}")

if __name__ == "__main__":
    asyncio.run(scan_pages())
