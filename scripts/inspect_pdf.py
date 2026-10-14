import pdfplumber

with pdfplumber.open("data/raw/un_r155.pdf") as pdf:
    print(f"Total pages: {len(pdf.pages)}")
    for i, p in enumerate(pdf.pages):
        t = p.extract_text() or ""
        tables = p.extract_tables()
        print(f"Page {i+1}: text_len={len(t)}, tables={len(tables)}, chars={len(p.chars)}")
        if len(t) > 0:
            print(f"   Preview: {t[:100].strip()}")
