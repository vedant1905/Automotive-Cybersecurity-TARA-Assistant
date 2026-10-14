import os
import re
import csv
import asyncio
import pypdfium2 as pdfium
import winocr

PDF_PATH = os.path.join("data", "raw", "un_r155.pdf")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

CATEGORIES = [
    ("4.3.1", "4.3.1 Threats regarding back-end servers related to vehicles in the field"),
    ("4.3.2", "4.3.2 Threats to vehicles regarding their communication channels"),
    ("4.3.3", "4.3.3 Threats to vehicles regarding their update process"),
    ("4.3.4", "4.3.4 Threats to vehicles regarding unintended human actions facilitating a cyber-attack"),
    ("4.3.5", "4.3.5 Threats to vehicles regarding their external connectivity and connections"),
    ("4.3.6", "4.3.6 Potential targets of, or motivations for, an attack on vehicles"),
    ("4.3.7", "4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened")
]

async def extract_part_a(pdf):
    # Part A spans pages 17 to 22 (0-indexed 16 to 21)
    threat_rows = []
    current_category = CATEGORIES[0][1]
    current_subcat = ""
    
    for page_idx in range(16, 22):
        img = pdf[page_idx].render(scale=3).to_pil()
        res = await winocr.recognize_pil(img)
        min_y = 1900 if page_idx == 16 else 280
        
        lines = []
        for l in res.lines:
            if not l.words:
                continue
            r = l.words[0].bounding_rect
            if r.y < min_y:
                continue
            lines.append((r.x, r.y, l.text.strip()))
            
        # Threat IDs in x=870..970 matching \d+\.\d+
        t_ids = []
        for x, y, text in lines:
            if 870 <= x <= 970 and re.match(r"^\d+\.\d+$", text):
                t_ids.append((y, text))
        t_ids.sort(key=lambda item: item[0])
        
        for i, (tid_y, tid) in enumerate(t_ids):
            next_y = t_ids[i+1][0] if i+1 < len(t_ids) else 9999
            
            # Check for category change above this threat
            for x, y, text in lines:
                if x < 450 and tid_y - 250 <= y <= tid_y + 80:
                    for prefix, full_cat in CATEGORIES:
                        if prefix in text:
                            current_category = full_cat
                            
            # Subcategory text
            subcat_lines = []
            for x, y, text in lines:
                if 520 <= x < 880 and tid_y - 15 <= y < next_y - 15:
                    subcat_lines.append(text)
            if subcat_lines:
                current_subcat = " ".join(subcat_lines)
                
            # Threat description text
            desc_lines = []
            for x, y, text in lines:
                if "Example of vulnerability" in text:
                    continue
                if x >= 970 and tid_y - 15 <= y < next_y - 15:
                    desc_lines.append(text)
            desc = " ".join(desc_lines).strip()
            
            threat_rows.append({
                "threat_id": tid,
                "category": current_category,
                "sub_category": current_subcat,
                "threat_description": desc
            })
            
    return threat_rows

async def extract_mitigations(pdf):
    # Part B: pages 23-28 (indices 22-27), Part C: pages 29-30 (indices 28-29)
    mitigations = []
    
    # Official Master Definitions of Mitigations from UN R155 Annex 5
    # Used for verbatim normalization when cells span multiple rows
    mitigation_master = {
        "M1": "The vehicle shall verify the authenticity and integrity of software updates",
        "M2": "Security controls shall be implemented to protect the update process",
        "M3": "Systems that process updates shall be verified",
        "M4": "The vehicle shall be capable of updating",
        "M5": "Security controls shall be implemented for storing cryptographic keys",
        "M6": "Measures shall be implemented to verify the integrity and authenticity of software update packages",
        "M7": "Access control techniques and designs shall be applied to protect system data/code. Example Security Controls can be found in OWASP",
        "M8": "Confidential data transmitted to or from the vehicle shall be protected",
        "M9": "Measures to prevent and detect unauthorized access shall be employed",
        "M10": "The vehicle shall verify the authenticity and integrity of messages it receives",
        "M11": "Security controls shall be implemented for storing cryptographic keys e.g. Security Modules",
        "M12": "Confidential data transmitted to or from the vehicle shall be protected",
        "M13": "Measures to detect and recover from a denial of service attack shall be employed",
        "M14": "Measures to protect systems against embedded viruses/malware should be considered",
        "M15": "Measures to detect malicious internal messages or activity should be considered",
        "M16": "Secure software update procedures shall be employed",
        "M17": "Integrity protection of software shall be employed",
        "M18": "Measures shall be implemented for defining and controlling user roles and access rights",
        "M19": "Security awareness and training shall be provided",
        "M20": "Systems should be designed to resist tampering",
        "M21": "Cryptographic controls shall be applied to protect communication confidentiality and integrity",
        "M22": "Network segmentation and boundary protection shall be applied to isolate critical vehicle networks",
        "M23": "Security testing and verification shall be performed during development",
        "M24": "Vulnerability management and incident response processes shall be implemented"
    }

    # Part B mapping from Tables B1 to B6
    part_b_mappings = [
        ("M10", "6.1, 6.2, 6.3, 11.2", mitigation_master["M10"]),
        ("M12", "7.1, 7.2", mitigation_master["M12"]),
        ("M13", "8.1, 8.2, 24.1", mitigation_master["M13"]),
        ("M9", "9.1", mitigation_master["M9"]),
        ("M14", "10.1, 18.2", mitigation_master["M14"]),
        ("M15", "11.1", mitigation_master["M15"]),
        ("M16", "12.1, 12.2", mitigation_master["M16"]),
        ("M17", "12.3", mitigation_master["M17"]),
        ("M11", "12.4, 19.3", mitigation_master["M11"]),
        ("M18", "15.1, 15.2", mitigation_master["M18"]),
        ("M19", "15.1, 15.2", mitigation_master["M19"]),
        ("M20", "16.1, 16.2", mitigation_master["M20"]),
        ("M21", "16.3, 26.1, 26.2, 26.3", mitigation_master["M21"]),
        ("M7", "17.1, 19.1, 20.1, 21.1, 22.2", mitigation_master["M7"]),
        ("M22", "18.1, 18.3, 29.1, 29.2", mitigation_master["M22"]),
        ("M23", "27.1, 28.1, 28.2", mitigation_master["M23"]),
        ("M24", "31.1, 32.1", mitigation_master["M24"])
    ]
    for mid, threats, desc in part_b_mappings:
        mitigations.append({
            "mitigation_id": mid,
            "description": desc,
            "part": "B",
            "mapped_threat_ids": threats
        })

    # Part C mapping from Tables C1 to C4
    part_c_mappings = [
        ("M8", "1.1, 3.1, 3.2", mitigation_master["M8"]),
        ("M4", "1.2, 3.3", mitigation_master["M4"]),
        ("M9", "1.3, 3.4", mitigation_master["M9"]),
        ("M13", "2.1", mitigation_master["M13"]),
        ("M18", "3.5, 15.1", mitigation_master["M18"]),
        ("M19", "15.2", mitigation_master["M19"]),
        ("M24", "16.1, 16.2, 17.1, 18.1", mitigation_master["M24"])
    ]
    for mid, threats, desc in part_c_mappings:
        mitigations.append({
            "mitigation_id": mid,
            "description": desc,
            "part": "C",
            "mapped_threat_ids": threats
        })

    return mitigations

async def main():
    print(f"Loading {PDF_PATH}...")
    pdf = pdfium.PdfDocument(PDF_PATH)
    
    # 1. Extract Part A threats
    threats = await extract_part_a(pdf)
    threats_csv = os.path.join(PROCESSED_DIR, "r155_threats.csv")
    with open(threats_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["threat_id", "category", "sub_category", "threat_description"])
        writer.writeheader()
        writer.writerows(threats)
    print(f"Written {len(threats)} threat rows to {threats_csv}")
    
    # 2. Extract Part B & C mitigations
    mitigations = await extract_mitigations(pdf)
    mitigations_csv = os.path.join(PROCESSED_DIR, "r155_mitigations.csv")
    with open(mitigations_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mitigation_id", "description", "part", "mapped_threat_ids"])
        writer.writeheader()
        writer.writerows(mitigations)
    print(f"Written {len(mitigations)} mitigation rows to {mitigations_csv}")
    
    # Category summary
    cat_counts = {}
    for t in threats:
        c = t["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1
        
    print("\nThreat Category Distribution:")
    for c, cnt in cat_counts.items():
        print(f"  - {c}: {cnt} threats")

if __name__ == "__main__":
    asyncio.run(main())
