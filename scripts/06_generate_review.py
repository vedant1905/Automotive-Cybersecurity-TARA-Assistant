import os
import sys
import json
import random

sys.path.insert(0, os.path.abspath("."))
LIBRARY_PATH = os.path.join("data", "library", "threat_library.json")
REVIEW_MD = os.path.join("data", "library", "REVIEW.md")

R155_OFFICIAL_URL = "https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf"

def get_capec_url(capec_id):
    num = capec_id.replace("CAPEC-", "")
    return f"https://capec.mitre.org/data/definitions/{num}.html"

def get_cwe_url(cwe_id):
    num = cwe_id.replace("CWE-", "")
    return f"https://cwe.mitre.org/data/definitions/{num}.html"

def generate_review():
    print("Generating human review report...")
    with open(LIBRARY_PATH, mode="r", encoding="utf-8") as f:
        library = json.load(f)

    # 1. Entries with needs_human_review == True
    review_entries = [e for e in library if e.get("needs_human_review") is True]
    
    # 2. 10 randomly chosen other entries
    other_entries = [e for e in library if e.get("needs_human_review") is not True]
    random.seed(42)
    sample_others = random.sample(other_entries, min(10, len(other_entries)))

    lines = []
    lines.append("# Automotive Cybersecurity Threat Library - Human Review Report")
    lines.append("")
    lines.append("This report audits the verified Threat Library (`data/library/threat_library.json`) for the Automotive Cybersecurity TARA Assistant.")
    lines.append("All entries below include direct official links to MITRE CAPEC, MITRE CWE, and the official EUR-Lex publication of UN Regulation No. 155.")
    lines.append("")
    lines.append("## 1. Summary Statistics")
    lines.append("")
    lines.append(f"- **Total Library Entries**: {len(library)}")
    lines.append(f"- **Entries with High Confidence**: {len(library) - len(review_entries)}")
    lines.append(f"- **Entries Flagged for Human Review**: {len(review_entries)}")
    lines.append(f"- **Audit Sampled High-Confidence Entries**: {len(sample_others)}")
    lines.append(f"- **Total Audited Entries in this Report**: {len(review_entries) + len(sample_others)}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. Flagged Entries Requiring Human Review (`needs_human_review = true`)")
    lines.append("")
    lines.append("The following entries have `medium` or `low` mapping confidence, or represent specialized domain concepts (e.g., RF jamming, supply chain hardware trojans, or multi-tenant storage leakage) that warrant expert validation:")
    lines.append("")

    for e in review_entries:
        lines.append(f"### [{e['id']}] {e['title']}")
        lines.append(f"- **UN R155 Threat ID**: [{e['r155_threat_id']}]({R155_OFFICIAL_URL}) (Annex 5 Part A)")
        lines.append(f"- **Category**: `{e['category']}`")
        lines.append(f"- **Mapping Confidence**: `{e['mapping_confidence'].upper()}`")
        lines.append(f"- **Affected Components**: {', '.join(e['affected_components'])}")
        lines.append(f"- **Affected Interfaces**: {', '.join(e['affected_interfaces'])}")
        lines.append(f"- **Technical Description**: {e['description']}")
        lines.append(f"- **Concrete Attack Scenario**: *\"{e['attack_example']}\"*")
        
        # CAPEC Links
        if e["capec"]:
            capec_links = [f"[{c['id']}: {c['name']}]({get_capec_url(c['id'])})" for c in e["capec"]]
            lines.append(f"- **MITRE CAPEC**: {', '.join(capec_links)}")
        else:
            lines.append("- **MITRE CAPEC**: *(None / Domain-specific)*")

        # CWE Links
        if e["cwe"]:
            cwe_links = [f"[{w['id']}: {w['name']}]({get_cwe_url(w['id'])})" for w in e["cwe"]]
            lines.append(f"- **MITRE CWE**: {', '.join(cwe_links)}")
        else:
            lines.append("- **MITRE CWE**: *(None / Hardware or procedural failure)*")

        # Mitigations
        if e["r155_mitigations"]:
            mits = [f"`{m['id']}` ({m['text_summary']})" for m in e["r155_mitigations"]]
            lines.append(f"- **UN R155 Mitigations**: {'; '.join(mits)}")
        else:
            lines.append("- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 3. Audited High-Confidence Sample Entries (10 Random Entries)")
    lines.append("")
    lines.append("Representative cross-section of high-confidence entries across different vehicle domains:")
    lines.append("")

    for e in sample_others:
        lines.append(f"### [{e['id']}] {e['title']}")
        lines.append(f"- **UN R155 Threat ID**: [{e['r155_threat_id']}]({R155_OFFICIAL_URL}) (Annex 5 Part A)")
        lines.append(f"- **Category**: `{e['category']}`")
        lines.append(f"- **Mapping Confidence**: `{e['mapping_confidence'].upper()}`")
        lines.append(f"- **Affected Components**: {', '.join(e['affected_components'])}")
        lines.append(f"- **Affected Interfaces**: {', '.join(e['affected_interfaces'])}")
        lines.append(f"- **Technical Description**: {e['description']}")
        lines.append(f"- **Concrete Attack Scenario**: *\"{e['attack_example']}\"*")
        
        capec_links = [f"[{c['id']}: {c['name']}]({get_capec_url(c['id'])})" for c in e["capec"]]
        lines.append(f"- **MITRE CAPEC**: {', '.join(capec_links)}")

        cwe_links = [f"[{w['id']}: {w['name']}]({get_cwe_url(w['id'])})" for w in e["cwe"]]
        lines.append(f"- **MITRE CWE**: {', '.join(cwe_links)}")

        if e["r155_mitigations"]:
            mits = [f"`{m['id']}` ({m['text_summary']})" for m in e["r155_mitigations"]]
            lines.append(f"- **UN R155 Mitigations**: {'; '.join(mits)}")
        else:
            lines.append("- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 4. Verification Check Instructions")
    lines.append("To independently verify this Threat Library at any time, execute the following commands in the virtual environment:")
    lines.append("```powershell")
    lines.append(".\\.venv\\Scripts\\python.exe scripts\\validate_library.py")
    lines.append(".\\.venv\\Scripts\\pytest.exe -v tests/test_library_validation.py")
    lines.append("```")
    lines.append("")

    with open(REVIEW_MD, mode="w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Successfully generated human review report at {REVIEW_MD}")

if __name__ == "__main__":
    generate_review()
