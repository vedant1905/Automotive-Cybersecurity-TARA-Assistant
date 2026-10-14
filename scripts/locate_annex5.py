import pypdfium2 as pdfium

pdf = pdfium.PdfDocument("data/raw/un_r155.pdf")
print("Total pages in PDF:", len(pdf))

for i, page in enumerate(pdf):
    text = page.get_textpage().get_text_range()
    text_lower = text.lower()
    if "annex 5" in text_lower:
        first_line = text.strip().split("\n")[0]
        print(f"Page {i+1}: {first_line[:80]}")
