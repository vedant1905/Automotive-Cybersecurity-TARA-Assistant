import os
import csv
import json
import pytest

LIBRARY_PATH = os.path.join("data", "library", "threat_library.json")
THREATS_CSV = os.path.join("data", "processed", "r155_threats.csv")
MITIGATIONS_CSV = os.path.join("data", "processed", "r155_mitigations.csv")
CAPEC_CSV = os.path.join("data", "processed", "capec.csv")
CWE_CSV = os.path.join("data", "processed", "cwe.csv")
VEHICLE_JSON = os.path.join("data", "system", "sample_vehicle.json")

@pytest.fixture(scope="session")
def library_data():
    assert os.path.exists(LIBRARY_PATH), f"File {LIBRARY_PATH} does not exist"
    with open(LIBRARY_PATH, mode="r", encoding="utf-8") as f:
        data = json.load(f)
    return data

@pytest.fixture(scope="session")
def threats_source():
    with open(THREATS_CSV, mode="r", encoding="utf-8") as f:
        return {r["threat_id"]: r for r in csv.DictReader(f)}

@pytest.fixture(scope="session")
def mitigations_source():
    with open(MITIGATIONS_CSV, mode="r", encoding="utf-8") as f:
        return {r["mitigation_id"]: r for r in csv.DictReader(f)}

@pytest.fixture(scope="session")
def capec_source():
    with open(CAPEC_CSV, mode="r", encoding="utf-8") as f:
        return {r["capec_id"]: r for r in csv.DictReader(f)}

@pytest.fixture(scope="session")
def cwe_source():
    with open(CWE_CSV, mode="r", encoding="utf-8") as f:
        return {r["cwe_id"]: r for r in csv.DictReader(f)}

@pytest.fixture(scope="session")
def vehicle_architecture():
    with open(VEHICLE_JSON, mode="r", encoding="utf-8") as f:
        v = json.load(f)
    return {
        "components": {c["name"] for c in v["components"]},
        "interfaces": {i["name"] for i in v["interfaces"]}
    }

def test_library_entry_count_bounds(library_data):
    """Entry count must be strictly between 40 and 60."""
    count = len(library_data)
    assert 40 <= count <= 60, f"Expected 40-60 entries, got {count}"

def test_unique_entry_ids(library_data):
    """Every library entry must have a unique sequential identifier."""
    ids = [entry["id"] for entry in library_data]
    assert len(ids) == len(set(ids)), "Found duplicate entry IDs in library"

def test_all_seven_categories_represented(library_data):
    """Every approved UN R155 category must have at least 1 entry."""
    all_7_categories = {
        "4.3.1 Threats regarding back-end servers related to vehicles in the field",
        "4.3.2 Threats to vehicles regarding their communication channels",
        "4.3.3 Threats to vehicles regarding their update process",
        "4.3.4 Threats to vehicles regarding unintended human actions facilitating a cyber-attack",
        "4.3.5 Threats to vehicles regarding their external connectivity and connections",
        "4.3.6 Potential targets of, or motivations for, an attack on vehicles",
        "4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened"
    }
    present_categories = {entry["category"] for entry in library_data}
    missing = all_7_categories - present_categories
    assert not missing, f"Missing categories with zero entries: {missing}"

def test_required_fields_and_structure(library_data):
    """Every entry must contain all required fields with non-empty values."""
    required_fields = [
        "id", "r155_threat_id", "category", "title", "description",
        "affected_components", "affected_interfaces", "attack_example",
        "capec", "cwe", "r155_mitigations", "mapping_confidence",
        "needs_human_review", "sources", "library_version"
    ]
    for entry in library_data:
        eid = entry.get("id")
        for field in required_fields:
            assert field in entry, f"Entry {eid} missing required field '{field}'"
            assert entry[field] is not None, f"Entry {eid} has null field '{field}'"
        assert len(entry["title"]) > 5, f"Entry {eid} title is too short"
        assert len(entry["description"]) > 20, f"Entry {eid} description is too short"
        assert len(entry["attack_example"]) > 10, f"Entry {eid} attack_example is too short"
        assert len(entry["affected_components"]) >= 1, f"Entry {eid} must affect at least 1 component"
        assert len(entry["affected_interfaces"]) >= 1, f"Entry {eid} must affect at least 1 interface"

def test_r155_threat_ids_and_categories_match_source(library_data, threats_source):
    """Zero invented R155 IDs; threat IDs and categories must match r155_threats.csv exactly."""
    for entry in library_data:
        eid = entry["id"]
        tid = entry["r155_threat_id"]
        assert tid in threats_source, f"Entry {eid} has unverified r155_threat_id '{tid}'"
        expected_cat = threats_source[tid]["category"]
        assert entry["category"] == expected_cat, f"Entry {eid} category mismatch"

def test_capec_ids_and_names_exact_match(library_data, capec_source):
    """Zero invented CAPEC IDs; names must match capec.csv verbatim."""
    for entry in library_data:
        eid = entry["id"]
        for c in entry["capec"]:
            cid = c["id"]
            cname = c["name"]
            assert cid in capec_source, f"Entry {eid} has unverified CAPEC ID '{cid}'"
            assert capec_source[cid]["name"] == cname, (
                f"Entry {eid} CAPEC name '{cname}' does not match official '{capec_source[cid]['name']}' verbatim"
            )

def test_cwe_ids_and_names_exact_match(library_data, cwe_source):
    """Zero invented CWE IDs; names must match cwe.csv verbatim."""
    for entry in library_data:
        eid = entry["id"]
        for w in entry["cwe"]:
            wid = w["id"]
            wname = w["name"]
            assert wid in cwe_source, f"Entry {eid} has unverified CWE ID '{wid}'"
            assert cwe_source[wid]["name"] == wname, (
                f"Entry {eid} CWE name '{wname}' does not match official '{cwe_source[wid]['name']}' verbatim"
            )

def test_r155_mitigations_match_source(library_data, mitigations_source):
    """Zero invented mitigation IDs; mitigations must exist in r155_mitigations.csv."""
    for entry in library_data:
        eid = entry["id"]
        for m in entry["r155_mitigations"]:
            mid = m["id"]
            assert mid in mitigations_source, f"Entry {eid} has unverified mitigation ID '{mid}'"

def test_affected_system_components_and_interfaces(library_data, vehicle_architecture):
    """All components and interfaces must be defined in sample_vehicle.json."""
    for entry in library_data:
        eid = entry["id"]
        for comp in entry["affected_components"]:
            assert comp in vehicle_architecture["components"], f"Entry {eid} references unknown component '{comp}'"
        for iface in entry["affected_interfaces"]:
            assert iface in vehicle_architecture["interfaces"], f"Entry {eid} references unknown interface '{iface}'"

def test_mapping_confidence_and_review_flags(library_data):
    """Entries with medium/low confidence or empty mappings must set needs_human_review=True."""
    for entry in library_data:
        eid = entry["id"]
        conf = entry["mapping_confidence"]
        needs_review = entry["needs_human_review"]
        assert conf in ["high", "medium", "low"], f"Entry {eid} invalid confidence '{conf}'"
        if conf in ["medium", "low"] or len(entry["capec"]) == 0 or len(entry["cwe"]) == 0:
            assert needs_review is True, f"Entry {eid} requires needs_human_review=True due to confidence/mapping"

def test_originality_of_descriptions(library_data, threats_source):
    """Descriptions and examples must be original, not verbatim copies of raw regulation text."""
    for entry in library_data:
        eid = entry["id"]
        raw = threats_source[entry["r155_threat_id"]]["threat_description"]
        assert entry["description"].strip().lower() != raw.strip().lower(), (
            f"Entry {eid} description is a verbatim copy of raw R155 text"
        )
