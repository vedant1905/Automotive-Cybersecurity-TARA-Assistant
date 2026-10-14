import os
import re
import csv

RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

CAPEC_RAW = os.path.join(RAW_DIR, "capec", "2000.csv")
CWE_RAW = os.path.join(RAW_DIR, "cwe", "2000.csv")

CAPEC_OUT = os.path.join(PROCESSED_DIR, "capec.csv")
CWE_OUT = os.path.join(PROCESSED_DIR, "cwe.csv")

def parse_related_cwes(raw_text):
    if not raw_text:
        return ""
    # MITRE related weaknesses may contain entries like "285::862" or "::285::" or comma/semicolon separated numbers
    # Extract all integer IDs from the field
    cwe_nums = re.findall(r"\b\d+\b", raw_text)
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for num in cwe_nums:
        cwe_id = f"CWE-{num}"
        if cwe_id not in seen:
            seen.add(cwe_id)
            deduped.append(cwe_id)
    return "; ".join(deduped)

def parse_capec():
    print(f"Parsing CAPEC from {CAPEC_RAW}...")
    entries = []
    with open(CAPEC_RAW, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_id = row.get("'ID") or row.get("ID", "")
            raw_id = raw_id.strip("' ").strip()
            if not raw_id or not raw_id.isdigit():
                continue
            
            capec_id = f"CAPEC-{raw_id}"
            name = (row.get("Name") or "").strip()
            desc = (row.get("Description") or "").strip()
            rel_cwes = parse_related_cwes(row.get("Related Weaknesses", ""))
            
            entries.append({
                "capec_id": capec_id,
                "name": name,
                "description": desc,
                "related_cwe_ids": rel_cwes
            })
            
    with open(CAPEC_OUT, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["capec_id", "name", "description", "related_cwe_ids"])
        writer.writeheader()
        writer.writerows(entries)
        
    print(f"Saved {len(entries)} CAPEC attack patterns to {CAPEC_OUT}")
    return entries

def parse_cwe():
    print(f"Parsing CWE from {CWE_RAW}...")
    entries = []
    with open(CWE_RAW, mode="r", encoding="utf-8", errors="ignore") as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw_id = row.get("CWE-ID") or row.get("ID", "")
            raw_id = raw_id.strip("' ").strip()
            if not raw_id or not raw_id.isdigit():
                continue
            
            cwe_id = f"CWE-{raw_id}"
            name = (row.get("Name") or "").strip()
            desc = (row.get("Description") or "").strip()
            
            entries.append({
                "cwe_id": cwe_id,
                "name": name,
                "description": desc
            })
            
    with open(CWE_OUT, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["cwe_id", "name", "description"])
        writer.writeheader()
        writer.writerows(entries)
        
    print(f"Saved {len(entries)} CWE weaknesses to {CWE_OUT}")
    return entries

def main():
    capec_entries = parse_capec()
    cwe_entries = parse_cwe()
    
    # Print sample of parsed entries
    print("\nCAPEC Samples:")
    for c in capec_entries[:3]:
        print(f"  {c['capec_id']}: {c['name']} (Related CWEs: {c['related_cwe_ids']})")
        
    print("\nCWE Samples:")
    for c in cwe_entries[:3]:
        print(f"  {c['cwe_id']}: {c['name']}")

if __name__ == "__main__":
    main()
