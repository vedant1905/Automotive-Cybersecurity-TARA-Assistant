import os
import sys
import csv
import json

sys.path.insert(0, os.path.abspath("."))
from scripts.propose_threat_scope import SELECTION

THREATS_CSV = os.path.join("data", "processed", "r155_threats.csv")
MITIGATIONS_CSV = os.path.join("data", "processed", "r155_mitigations.csv")
CAPEC_CSV = os.path.join("data", "processed", "capec.csv")
CWE_CSV = os.path.join("data", "processed", "cwe.csv")
OUTPUT_JSON = os.path.join("data", "processed", "mapped_threats.json")

# Verified mappings for all 50 selected threats
# Every CAPEC ID and CWE ID is verified against capec.csv and cwe.csv
THREAT_MAPPING_RULES = {
    # 4.3.1 Threats regarding back-end servers
    "1.1": {
        "capec_ids": ["CAPEC-122"],
        "cwe_ids": ["CWE-269"],
        "confidence": "high"
    },
    "1.2": {
        "capec_ids": ["CAPEC-66", "CAPEC-115"],
        "cwe_ids": ["CWE-89", "CWE-287"],
        "confidence": "high"
    },
    "1.3": {
        "capec_ids": ["CAPEC-457"],
        "cwe_ids": ["CWE-1299"],
        "confidence": "high"
    },
    "2.1": {
        "capec_ids": ["CAPEC-125"],
        "cwe_ids": ["CWE-404"],
        "confidence": "high"
    },
    "3.1": {
        "capec_ids": ["CAPEC-122"],
        "cwe_ids": ["CWE-269"],
        "confidence": "high"
    },
    "3.2": {
        "capec_ids": ["CAPEC-546"],
        "cwe_ids": ["CWE-284"],
        "confidence": "medium"
    },
    "3.3": {
        "capec_ids": ["CAPEC-66", "CAPEC-115"],
        "cwe_ids": ["CWE-89", "CWE-287"],
        "confidence": "high"
    },
    # 4.3.2 Threats to vehicles regarding communication channels
    "4.1": {
        "capec_ids": ["CAPEC-151", "CAPEC-148"],
        "cwe_ids": ["CWE-287", "CWE-345"],
        "confidence": "high"
    },
    "4.2": {
        "capec_ids": ["CAPEC-151"],
        "cwe_ids": ["CWE-287"],
        "confidence": "medium"
    },
    "5.1": {
        "capec_ids": ["CAPEC-242"],
        "cwe_ids": ["CWE-94"],
        "confidence": "high"
    },
    "5.2": {
        "capec_ids": ["CAPEC-153"],
        "cwe_ids": ["CWE-20"],
        "confidence": "high"
    },
    "5.3": {
        "capec_ids": ["CAPEC-100"],
        "cwe_ids": ["CWE-120"],
        "confidence": "high"
    },
    "5.4": {
        "capec_ids": ["CAPEC-153"],
        "cwe_ids": ["CWE-20"],
        "confidence": "medium"
    },
    "5.5": {
        "capec_ids": ["CAPEC-242", "CAPEC-153"],
        "cwe_ids": ["CWE-94", "CWE-20"],
        "confidence": "high"
    },
    "6.1": {
        "capec_ids": ["CAPEC-153"],
        "cwe_ids": ["CWE-20"],
        "confidence": "high"
    },
    "6.2": {
        "capec_ids": ["CAPEC-94"],
        "cwe_ids": ["CWE-300"],
        "confidence": "high"
    },
    "6.3": {
        "capec_ids": ["CAPEC-60"],
        "cwe_ids": ["CWE-294"],
        "confidence": "high"
    },
    "7.1": {
        "capec_ids": ["CAPEC-157", "CAPEC-651"],
        "cwe_ids": ["CWE-311", "CWE-200"],
        "confidence": "high"
    },
    "7.2": {
        "capec_ids": ["CAPEC-122"],
        "cwe_ids": ["CWE-269"],
        "confidence": "high"
    },
    "8.1": {
        "capec_ids": ["CAPEC-125"],
        "cwe_ids": ["CWE-404"],
        "confidence": "high"
    },
    "9.1": {
        "capec_ids": ["CAPEC-233"],
        "cwe_ids": ["CWE-269"],
        "confidence": "high"
    },
    "11.1": {
        "capec_ids": ["CAPEC-242", "CAPEC-151"],
        "cwe_ids": ["CWE-94", "CWE-287"],
        "confidence": "high"
    },
    # 4.3.3 Threats regarding update process
    "12.1": {
        "capec_ids": ["CAPEC-186", "CAPEC-657"],
        "cwe_ids": ["CWE-494"],
        "confidence": "high"
    },
    "12.2": {
        "capec_ids": ["CAPEC-186", "CAPEC-184"],
        "cwe_ids": ["CWE-494"],
        "confidence": "high"
    },
    "12.3": {
        "capec_ids": ["CAPEC-184"],
        "cwe_ids": ["CWE-494"],
        "confidence": "high"
    },
    "12.4": {
        "capec_ids": ["CAPEC-97", "CAPEC-20"],
        "cwe_ids": ["CWE-327", "CWE-326"],
        "confidence": "high"
    },
    "13.1": {
        "capec_ids": ["CAPEC-125"],
        "cwe_ids": ["CWE-404"],
        "confidence": "high"
    },
    # 4.3.4 Threats regarding unintended human actions
    "15.1": {
        "capec_ids": ["CAPEC-416", "CAPEC-457"],
        "cwe_ids": ["CWE-1299"],
        "confidence": "high"
    },
    "15.2": {
        "capec_ids": ["CAPEC-180"],
        "cwe_ids": ["CWE-732"],
        "confidence": "medium"
    },
    # 4.3.5 Threats regarding external connectivity
    "16.1": {
        "capec_ids": ["CAPEC-395", "CAPEC-60"],
        "cwe_ids": ["CWE-294"],
        "confidence": "high"
    },
    "16.2": {
        "capec_ids": ["CAPEC-610", "CAPEC-609"],
        "cwe_ids": ["CWE-311"],
        "confidence": "high"
    },
    "16.3": {
        "capec_ids": ["CAPEC-603"],
        "cwe_ids": [],
        "confidence": "low"
    },
    "17.1": {
        "capec_ids": ["CAPEC-242", "CAPEC-100"],
        "cwe_ids": ["CWE-94", "CWE-120"],
        "confidence": "high"
    },
    "18.1": {
        "capec_ids": ["CAPEC-457", "CAPEC-242"],
        "cwe_ids": ["CWE-1299", "CWE-94"],
        "confidence": "high"
    },
    "18.2": {
        "capec_ids": ["CAPEC-457", "CAPEC-542"],
        "cwe_ids": ["CWE-1299"],
        "confidence": "high"
    },
    "18.3": {
        "capec_ids": ["CAPEC-184", "CAPEC-153"],
        "cwe_ids": ["CWE-494", "CWE-20"],
        "confidence": "high"
    },
    # 4.3.6 Potential targets of or motivations for an attack
    "19.1": {
        "capec_ids": ["CAPEC-188"],
        "cwe_ids": ["CWE-1278"],
        "confidence": "high"
    },
    "19.3": {
        "capec_ids": ["CAPEC-37"],
        "cwe_ids": ["CWE-311"],
        "confidence": "high"
    },
    "20.1": {
        "capec_ids": ["CAPEC-153", "CAPEC-184"],
        "cwe_ids": ["CWE-20", "CWE-494"],
        "confidence": "high"
    },
    "20.3": {
        "capec_ids": ["CAPEC-180"],
        "cwe_ids": ["CWE-732"],
        "confidence": "medium"
    },
    "20.5": {
        "capec_ids": ["CAPEC-153"],
        "cwe_ids": ["CWE-20"],
        "confidence": "medium"
    },
    "21.1": {
        "capec_ids": ["CAPEC-93"],
        "cwe_ids": ["CWE-117"],
        "confidence": "high"
    },
    "22.2": {
        "capec_ids": ["CAPEC-542", "CAPEC-184"],
        "cwe_ids": ["CWE-494"],
        "confidence": "high"
    },
    "24.1": {
        "capec_ids": ["CAPEC-125"],
        "cwe_ids": ["CWE-404"],
        "confidence": "high"
    },
    # 4.3.7 Potential vulnerabilities
    "26.1": {
        "capec_ids": ["CAPEC-20", "CAPEC-97"],
        "cwe_ids": ["CWE-326", "CWE-327"],
        "confidence": "high"
    },
    "26.2": {
        "capec_ids": ["CAPEC-97", "CAPEC-20"],
        "cwe_ids": ["CWE-327", "CWE-326"],
        "confidence": "high"
    },
    "27.1": {
        "capec_ids": ["CAPEC-438"],
        "cwe_ids": [],
        "confidence": "low"
    },
    "28.1": {
        "capec_ids": ["CAPEC-100"],
        "cwe_ids": ["CWE-120", "CWE-119"],
        "confidence": "high"
    },
    "28.2": {
        "capec_ids": ["CAPEC-190"],
        "cwe_ids": ["CWE-912"],
        "confidence": "high"
    },
    "29.2": {
        "capec_ids": ["CAPEC-180"],
        "cwe_ids": ["CWE-732"],
        "confidence": "high"
    }
}

def map_threats():
    print(f"Mapping threats using processed CSV files...")
    with open(THREATS_CSV, mode="r", encoding="utf-8") as f:
        threats_dict = {r["threat_id"]: r for r in csv.DictReader(f)}

    with open(CAPEC_CSV, mode="r", encoding="utf-8") as f:
        capec_dict = {r["capec_id"]: r for r in csv.DictReader(f)}

    with open(CWE_CSV, mode="r", encoding="utf-8") as f:
        cwe_dict = {r["cwe_id"]: r for r in csv.DictReader(f)}

    with open(MITIGATIONS_CSV, mode="r", encoding="utf-8") as f:
        mitigations_list = list(csv.DictReader(f))

    # Map mitigations
    threat_mitigations = {}
    for m in mitigations_list:
        m_id = m["mitigation_id"]
        m_desc = m["description"]
        mapped_tids = [x.strip() for x in m["mapped_threat_ids"].split(",") if x.strip()]
        for tid in mapped_tids:
            cur_list = threat_mitigations.setdefault(tid, [])
            if not any(x["id"] == m_id for x in cur_list):
                cur_list.append({
                    "id": m_id,
                    "text_summary": m_desc
                })

    mapped_results = []
    
    for item in SELECTION:
        tid = item["r155_threat_id"]
        t_info = threats_dict[tid]
        rule = THREAT_MAPPING_RULES[tid]
        
        # Verify and extract CAPEC directly from capec_dict
        capec_list = []
        for cid in rule["capec_ids"]:
            assert cid in capec_dict, f"CAPEC ID {cid} missing from capec.csv!"
            capec_list.append({
                "id": cid,
                "name": capec_dict[cid]["name"]
            })
            
        # Verify and extract CWE directly from cwe_dict
        cwe_list = []
        for wid in rule["cwe_ids"]:
            assert wid in cwe_dict, f"CWE ID {wid} missing from cwe.csv!"
            cwe_list.append({
                "id": wid,
                "name": cwe_dict[wid]["name"]
            })
            
        # Get mitigations
        mits = threat_mitigations.get(tid, [])
        
        confidence = rule["confidence"]
        needs_review = (confidence in ["medium", "low"]) or (len(capec_list) == 0) or (len(cwe_list) == 0)
        
        mapped_results.append({
            "r155_threat_id": tid,
            "category": t_info["category"],
            "sub_category": t_info["sub_category"],
            "r155_description": t_info["threat_description"],
            "affected_components": item["affected_components"],
            "affected_interfaces": item["affected_interfaces"],
            "capec": capec_list,
            "cwe": cwe_list,
            "r155_mitigations": mits,
            "mapping_confidence": confidence,
            "needs_human_review": needs_review
        })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(mapped_results, f, indent=2)

    print(f"Successfully mapped {len(mapped_results)} threats to {OUTPUT_JSON}.")
    review_count = sum(1 for x in mapped_results if x["needs_human_review"])
    print(f"  - High confidence: {len(mapped_results) - review_count}")
    print(f"  - Needing human review (medium/low): {review_count}")

if __name__ == "__main__":
    map_threats()
