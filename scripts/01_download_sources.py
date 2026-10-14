import os
import sys
import hashlib
import zipfile
import datetime
import requests

RAW_DIR = os.path.join("data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(os.path.join("data", "processed"), exist_ok=True)
os.makedirs(os.path.join("data", "system"), exist_ok=True)
os.makedirs(os.path.join("data", "library"), exist_ok=True)
os.makedirs("tests", exist_ok=True)

SOURCES = [
    {
        "name": "UN Regulation No. 155 (Annex 5)",
        "url": "https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf",
        "filename": "un_r155.pdf",
        "version": "Regulation (EU) 2025/5 / UN R155 OJ L 2025/5",
        "type": "pdf"
    },
    {
        "name": "CAPEC Comprehensive Dictionary (View 2000)",
        "url": "https://capec.mitre.org/data/csv/2000.csv.zip",
        "filename": "capec_2000.csv.zip",
        "version": "CAPEC Version 3.9 (View 2000)",
        "type": "zip"
    },
    {
        "name": "CWE Comprehensive View (View 2000)",
        "url": "https://cwe.mitre.org/data/csv/2000.csv.zip",
        "filename": "cwe_2000.csv.zip",
        "version": "CWE Version 4.20 (View 2000)",
        "type": "zip"
    }
]

def calculate_sha256(filepath):
    sha = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)
    return sha.hexdigest()

def download_file(url, target_path):
    print(f"Downloading {url} -> {target_path}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, headers=headers, stream=True, timeout=60)
    r.raise_for_status()
    with open(target_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=16384):
            f.write(chunk)
    print(f"Downloaded {target_path} ({os.path.getsize(target_path)} bytes)")

def main():
    download_records = []
    
    for src in SOURCES:
        target_path = os.path.join(RAW_DIR, src["filename"])
        download_file(src["url"], target_path)
        sha256 = calculate_sha256(target_path)
        
        extracted_files = []
        if src["type"] == "zip":
            subfolder = "capec" if "capec" in src["filename"] else "cwe"
            subpath = os.path.join(RAW_DIR, subfolder)
            os.makedirs(subpath, exist_ok=True)
            with zipfile.ZipFile(target_path, 'r') as zip_ref:
                names = zip_ref.namelist()
                print(f"Archive {src['filename']} contains: {names}")
                zip_ref.extractall(subpath)
                extracted_files = [os.path.join(subfolder, n) for n in names]
                
        download_records.append({
            "name": src["name"],
            "url": src["url"],
            "filename": src["filename"],
            "extracted_files": extracted_files,
            "version": src["version"],
            "sha256": sha256,
            "download_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        })

    # Generate SOURCES.md
    sources_md_path = os.path.join(RAW_DIR, "SOURCES.md")
    with open(sources_md_path, "w", encoding="utf-8") as f:
        f.write("# Data Sources Provenance Log\n\n")
        f.write("| Source Name | Official Download URL | Version / Identifier | Download Date (UTC) | File Name | SHA-256 Checksum |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for rec in download_records:
            f.write(f"| {rec['name']} | [{rec['url']}]({rec['url']}) | {rec['version']} | {rec['download_date']} | {rec['filename']} | `{rec['sha256']}` |\n")
        
        f.write("\n\n## Extracted Files\n")
        for rec in download_records:
            if rec["extracted_files"]:
                f.write(f"- **{rec['name']}**: {', '.join(rec['extracted_files'])}\n")

    print(f"Provenance log written to {sources_md_path}")

if __name__ == "__main__":
    main()
