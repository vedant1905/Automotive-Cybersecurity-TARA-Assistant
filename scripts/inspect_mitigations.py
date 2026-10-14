import asyncio
import re
import pypdfium2 as pdfium
import winocr

async def inspect_mitigations():
    pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
    
    # Part B spans pages 23 to 28 (indices 22 to 27)
    # Part C spans pages 29 to 30 (indices 28 to 29)
    print("--- Inspecting Part B (Vehicle Mitigations) ---")
    for page_idx in range(22, 28):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        lines = [l for l in res.lines if l.words]
        # Look for mitigation IDs (like M1, M2, etc. or numbered mitigations)
        m_lines = [l.text for l in lines if re.match(r"^(M\d+|[A-Z]\d+|\d+)\b", l.text)]
        print(f"Page {page_idx+1}: {len(lines)} lines, sample matches: {m_lines[:5]}")

    print("\n--- Inspecting Part C (Outside Vehicle Mitigations) ---")
    for page_idx in range(28, 30):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        lines = [l for l in res.lines if l.words]
        m_lines = [l.text for l in lines if re.match(r"^(M\d+|[A-Z]\d+|\d+)\b", l.text)]
        print(f"Page {page_idx+1}: {len(lines)} lines, sample matches: {m_lines[:5]}")

if __name__ == "__main__":
    asyncio.run(inspect_mitigations())
