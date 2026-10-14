import os
import sys
import csv
import json

THREATS_CSV = os.path.join("data", "processed", "r155_threats.csv")
MITIGATIONS_CSV = os.path.join("data", "processed", "r155_mitigations.csv")
CAPEC_CSV = os.path.join("data", "processed", "capec.csv")
CWE_CSV = os.path.join("data", "processed", "cwe.csv")
VEHICLE_JSON = os.path.join("data", "system", "sample_vehicle.json")
LIBRARY_JSON = os.path.join("data", "library", "threat_library.json")

REQUIRED_FIELDS = [
    "id",
    "r155_threat_id",
    "category",
    "title",
    "description",
    "affected_components",
    "affected_interfaces",
    "attack_example",
    "capec",
    "cwe",
    "r155_mitigations",
    "mapping_confidence",
    "needs_human_review",
    "sources",
    "library_version"
]

def validate_library():
    errors = []
    
    if not os.path.exists(LIBRARY_JSON):
        print(f"FATAL: Library file does not exist at {LIBRARY_JSON}")
        sys.exit(1)
        
    with open(LIBRARY_JSON, mode="r", encoding="utf-8") as f:
        library = json.load(f)

    # 1. Entry count must be within 40-60
    count = len(library)
    print(f"Validating threat library ({count} entries)...")
    if not (40 <= count <= 60):
        errors.append(f"Library entry count {count} is outside the required 40-60 range.")

    # Load source files
    with open(THREATS_CSV, mode="r", encoding="utf-8") as f:
        threats_dict = {r["threat_id"]: r for r in csv.DictReader(f)}

    with open(MITIGATIONS_CSV, mode="r", encoding="utf-8") as f:
        mitigations_dict = {r["mitigation_id"]: r for r in csv.DictReader(f)}

    with open(CAPEC_CSV, mode="r", encoding="utf-8") as f:
        capec_dict = {r["capec_id"]: r for r in csv.DictReader(f)}

    with open(CWE_CSV, mode="r", encoding="utf-8") as f:
        cwe_dict = {r["cwe_id"]: r for r in csv.DictReader(f)}

    with open(VEHICLE_JSON, mode="r", encoding="utf-8") as f:
        v_data = json.load(f)
        valid_components = {c["name"] for c in v_data["components"]}
        valid_interfaces = {i["name"] for i in v_data["interfaces"]}

    categories_present = set()
    all_7_categories = {
        "4.3.1 Threats regarding back-end servers related to vehicles in the field",
        "4.3.2 Threats to vehicles regarding their communication channels",
        "4.3.3 Threats to vehicles regarding their update process",
        "4.3.4 Threats to vehicles regarding unintended human actions facilitating a cyber-attack",
        "4.3.5 Threats to vehicles regarding their external connectivity and connections",
        "4.3.6 Potential targets of, or motivations for, an attack on vehicles",
        "4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened"
    }

    seen_ids = set()

    for idx, entry in enumerate(library, 1):
        eid = entry.get("id", f"ENTRY-{idx}")
        
        # Check unique IDs
        if eid in seen_ids:
            errors.append(f"Duplicate entry ID: {eid}")
        seen_ids.add(eid)

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in entry:
                errors.append(f"Entry {eid} is missing required field: '{field}'")
            elif entry[field] is None:
                errors.append(f"Entry {eid} has null field: '{field}'")
            elif isinstance(entry[field], (str, list)) and len(entry[field]) == 0 and field not in ["capec", "cwe", "r155_mitigations"]:
                errors.append(f"Entry {eid} has empty required field: '{field}'")

        # Validate R155 Threat ID
        r155_id = entry.get("r155_threat_id")
        if r155_id not in threats_dict:
            errors.append(f"Entry {eid} has invalid r155_threat_id '{r155_id}' (not found in {THREATS_CSV})")
        else:
            cat = entry.get("category")
            expected_cat = threats_dict[r155_id]["category"]
            if cat != expected_cat:
                errors.append(f"Entry {eid} category mismatch: '{cat}' vs expected '{expected_cat}'")
            categories_present.add(expected_cat)

        # Validate affected components and interfaces against sample_vehicle.json
        for comp in entry.get("affected_components", []):
            if comp not in valid_components:
                errors.append(f"Entry {eid} component '{comp}' not defined in {VEHICLE_JSON}")

        for iface in entry.get("affected_interfaces", []):
            if iface not in valid_interfaces:
                errors.append(f"Entry {eid} interface '{iface}' not defined in {VEHICLE_JSON}")

        # Validate CAPEC entries
        for capec_item in entry.get("capec", []):
            cid = capec_item.get("id")
            cname = capec_item.get("name")
            if cid not in capec_dict:
                errors.append(f"Entry {eid} CAPEC ID '{cid}' does not exist in {CAPEC_CSV}")
            elif capec_dict[cid]["name"] != cname:
                errors.append(f"Entry {eid} CAPEC name '{cname}' does not match official name '{capec_dict[cid]['name']}' verbatim")

        # Validate CWE entries
        for cwe_item in entry.get("cwe", []):
            wid = cwe_item.get("id")
            wname = cwe_item.get("name")
            if wid not in cwe_dict:
                errors.append(f"Entry {eid} CWE ID '{wid}' does not exist in {CWE_CSV}")
            elif cwe_dict[wid]["name"] != wname:
                errors.append(f"Entry {eid} CWE name '{wname}' does not match official name '{cwe_dict[wid]['name']}' verbatim")

        # Validate R155 Mitigations
        for mit in entry.get("r155_mitigations", []):
            mid = mit.get("id")
            if mid not in mitigations_dict:
                errors.append(f"Entry {eid} Mitigation ID '{mid}' does not exist in {MITIGATIONS_CSV}")

        # Validate confidence & human review flag
        conf = entry.get("mapping_confidence")
        if conf not in ["high", "medium", "low"]:
            errors.append(f"Entry {eid} invalid mapping_confidence: '{conf}'")
        needs_review = entry.get("needs_human_review")
        if conf in ["medium", "low"] and not needs_review:
            errors.append(f"Entry {eid} has confidence '{conf}' but needs_human_review is False")

        # Originality checks
        desc = entry.get("description", "")
        if r155_id in threats_dict:
            raw_text = threats_dict[r155_id]["threat_description"]
            if desc.strip().lower() == raw_text.strip().lower():
                errors.append(f"Entry {eid} description is a verbatim copy of the raw R155 text.")

    # 4. Check category coverage
    missing_categories = all_7_categories - categories_present
    if missing_categories:
        errors.append(f"The following required categories have zero entries: {missing_categories}")

    if errors:
        print(f"\nVALIDATION FAILED with {len(errors)} error(s):")
        for err in errors:
            print(f"  - [FAIL] {err}")
        sys.exit(1)
    else:
        print(f"\nALL CHECKS PASSED: Threat library is 100% verified and compliant!")
        print(f"  - Total entries: {len(library)}")
        print(f"  - Categories covered: {len(categories_present)} / 7")
        print(f"  - Zero invented CAPEC/CWE/R155 IDs verified.")
        sys.exit(0)

if __name__ == "__main__":
    validate_library()
