import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DOCS_DIR = os.path.join("docs")
OUTPUT_DOCX = os.path.join(DOCS_DIR, "PROJECT_SYNOPSIS.docx")

# Color palette: Professional Automotive / Enterprise Deep Blue
COLOR_PRIMARY = RGBColor(14, 43, 92)      # Deep Navy #0E2B5C
COLOR_SECONDARY = RGBColor(37, 99, 235)   # Cobalt Blue #2563EB
COLOR_TEXT_DARK = RGBColor(30, 41, 59)    # Slate Dark #1E293B
COLOR_MUTED = RGBColor(100, 116, 139)     # Slate Gray #64748B

def set_cell_background(cell, fill_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tc_pr.append(tc_mar)

def add_styled_heading(doc, text, level):
    h = doc.add_heading(level=level)
    run = h.add_run(text)
    run.font.name = "Calibri"
    if level == 1:
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.color.rgb = COLOR_PRIMARY
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(6)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.bold = True
        run.font.color.rgb = COLOR_SECONDARY
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(4)
    elif level == 3:
        run.font.size = Pt(11)
        run.font.bold = True
        run.font.color.rgb = COLOR_TEXT_DARK
        h.paragraph_format.space_before = Pt(6)
        h.paragraph_format.space_after = Pt(2)
    return h

def add_body_p(doc, text, bold_prefix="", space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT_DARK
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = COLOR_TEXT_DARK
    return p

def add_bullet_item(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_TEXT_DARK
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10.5)
    r_body.font.color.rgb = COLOR_TEXT_DARK
    return p

def format_table(table, col_widths, headers, data):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "0E2B5C")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(10)
            r.font.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)

    # Data rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.add_row().cells
        bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
                r.font.color.rgb = COLOR_TEXT_DARK

    # Column widths
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)

def generate_synopsis():
    os.makedirs(DOCS_DIR, exist_ok=True)
    doc = docx.Document()

    # Set 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # ==========================
    # 1. TITLE & COVER HEADER
    # ==========================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("AUTOMOTIVE CYBERSECURITY TARA ASSISTANT")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("An AI-Powered Threat Analysis & Risk Assessment Platform Grounded in UN R155, ISO/SAE 21434, and MITRE CAPEC/CWE Taxonomy")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = COLOR_SECONDARY

    # Meta banner table
    tbl_meta = doc.add_table(rows=1, cols=3)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_cells = tbl_meta.rows[0].cells
    meta_cells[0].text = "Project Track:\nTata TechPulse Capstone"
    meta_cells[1].text = "Domain:\nAutomotive E/E Cybersecurity"
    meta_cells[2].text = "Project Phase:\nMilestone 0 Completed"
    for cell in meta_cells:
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Calibri"
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = COLOR_PRIMARY
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================
    # 2. EXECUTIVE SUMMARY
    # ==========================
    add_styled_heading(doc, "1. Executive Summary", level=1)
    add_body_p(doc, 
        "The automotive industry is undergoing a monumental transition toward Software-Defined Vehicles (SDVs), characterized by pervasive cloud connectivity, Over-The-Air (OTA) firmware pipelines, advanced driver assistance systems (ADAS), and interconnected Electronic Control Units (ECUs). Concurrently, global regulatory bodies have mandated stringent cybersecurity compliance. United Nations Regulation No. 155 (UN R155) establishes that vehicle manufacturers (OEMs) must implement a certified Cyber Security Management System (CSMS) and perform rigorous Threat Analysis and Risk Assessment (TARA) compliant with ISO/SAE 21434 to achieve vehicle type approval.")
    add_body_p(doc,
        "However, conducting manual TARA for modern vehicle architectures is highly complex, resource-intensive, and prone to human oversight. Conversely, relying on generic commercial Large Language Models (LLMs) poses grave risks due to 'hallucinations'—the fabrication of non-existent Common Weakness Enumeration (CWE) or Common Attack Pattern Enumeration and Classification (CAPEC) identifiers, arbitrary risk ratings, and inaccurate regulatory citations. In safety-critical automotive systems, hallucinated data invalidates homologation audits and compromises passenger safety.")
    add_body_p(doc,
        "The Automotive Cybersecurity TARA Assistant solves this industry bottleneck. It is an agentic, retrieval-augmented intelligence system engineered to assist automotive cybersecurity engineers in identifying threats, evaluating attack feasibility, and computing ISO/SAE 21434 risk metrics. Crucially, the platform enforces a non-negotiable 'Zero Hallucinated IDs' rule: every regulatory clause, attack pattern, and weakness is verified through an authentic ground-truth knowledge library parsed directly from official UN, MITRE, and ISO sources.")

    # ==========================
    # 3. PROBLEM STATEMENT & MOTIVATION
    # ==========================
    add_styled_heading(doc, "2. Problem Statement & Motivation", level=1)
    add_body_p(doc,
        "Modern connected vehicles possess an expansive attack surface spanning wireless edge domains (Cellular 4G/5G, Wi-Fi, Bluetooth, GNSS), physical diagnostic ports (OBD-II via UDS), infotainment systems, and internal control networks (CAN, CAN-FD, Automotive Ethernet). An unmitigated vulnerability in a single peripheral controller—such as an Infotainment Head Unit (IVI) or Telematics Control Unit (TCU)—can be leveraged by adversaries to pivot into safety-critical domains (Powertrain and Braking controllers).")
    add_body_p(doc,
        "Current automotive security workflows suffer from three major industry challenges:", bold_prefix="Industry Pain Points: ")
    add_bullet_item(doc, "Manual engineering assessments take hundreds of man-hours per vehicle program, delaying development cycles.", bold_prefix="High Complexity & Time Consumption: ")
    add_bullet_item(doc, "TARA results frequently vary between individual analysts due to subjective impact ratings and incomplete threat taxonomies.", bold_prefix="Inconsistent Risk Assessments: ")
    add_bullet_item(doc, "Under UN R155, vehicle type approval requires demonstrable evidence that all applicable Annex 5 threats and mitigations have been formally addressed. An audit failure prevents vehicle sale in over 60 UNECE member states.", bold_prefix="Strict Regulatory Mandates: ")
    add_bullet_item(doc, "Existing generative AI tools invent non-existent CVEs, misquote regulatory articles, and generate plausible-sounding but unverified mitigations.", bold_prefix="Unacceptable AI Hallucinations: ")

    # ==========================
    # 4. PROJECT OBJECTIVES & SCOPE
    # ==========================
    add_styled_heading(doc, "3. Project Objectives & Scope", level=1)
    add_body_p(doc,
        "The primary objective of this Tata TechPulse capstone project is to develop a trustworthy, auditable, and automated Automotive Cybersecurity TARA Assistant. The project encompasses four primary technical pillars:")
    
    add_bullet_item(doc, "Construct an authenticated, 50-entry ground-truth threat library covering all 7 categories of UN R155 Annex 5, officially linked to MITRE CAPEC attack patterns, MITRE CWE weaknesses, and UN R155 mitigations. Enforce 100% programmatic verification with zero invented IDs.", bold_prefix="Objective 1 (Milestone 0 - Complete): ")
    add_bullet_item(doc, "Ingest the verified threat library into a high-performance vector database (ChromaDB) using domain-adapted dense embeddings to enable sub-second semantic retrieval across vehicle components, interfaces, and threat vectors.", bold_prefix="Objective 2 (Milestone 1 - Ingestion & RAG): ")
    add_bullet_item(doc, "Implement a structured TARA reasoning pipeline adhering to ISO/SAE 21434 Section 15. The engine automates Asset Identification, Threat Scenario Generation, Attack Feasibility Rating (via Attack Potential factors), Impact Assessment across SFOP (Safety, Financial, Operational, Privacy) dimensions, and Risk Value determination (1 to 5).", bold_prefix="Objective 3 (Milestone 2 - TARA Engine): ")
    add_bullet_item(doc, "Provide an engineer-facing assistant interface that produces audit-ready compliance documentation, traceability matrices, and clickable verification reports for vehicle type-approval submissions.", bold_prefix="Objective 4 (Milestone 3 - Assistant & Reporting): ")

    # ==========================
    # 5. TARGET VEHICLE ARCHITECTURE
    # ==========================
    add_styled_heading(doc, "4. Target Vehicle E/E Architecture Scope", level=1)
    add_body_p(doc,
        "To ensure concrete engineering validity, the assistant is evaluated against a reference Connected and Automated Vehicle (CAV) Electrical/Electronic (E/E) architecture defined in the project data schema:")
    
    # Table of components
    tbl_comp = doc.add_table(rows=1, cols=4)
    col_w = [1.8, 1.4, 1.4, 2.0]
    headers = ["Component Name", "Trust Zone", "Primary Interfaces", "Key Critical Functions"]
    data_comp = [
        ["Telematics Control Unit (TCU)", "Wireless Edge Domain", "Cellular, Wi-Fi, BLE, CAN, Ethernet", "Remote OTA reception, telemetry, emergency eCall"],
        ["Central Gateway (CGW)", "Core Security Gateway", "CAN, Automotive Ethernet, OBD-II", "Inter-domain routing, firewall filtering, SecOC, diagnostics"],
        ["Infotainment Head Unit (IVI)", "Infotainment Domain", "USB, Bluetooth, Wi-Fi, Ethernet", "User media display, smartphone projection, consumer apps"],
        ["OBD-II Diagnostic Port", "Physical Maintenance", "CAN, UDS over CAN", "Dealership servicing, ECU flashing, fault diagnosis"],
        ["Powertrain & Brake ECUs", "Chassis Control (Critical)", "High-Speed CAN", "Throttle actuation, engine torque management, ABS/ESC"],
        ["OTA Backend Server & API", "Cloud / Remote Tier", "Internet / REST API, Cellular", "Firmware signing, campaign dispatch, fleet telemetry"]
    ]
    format_table(tbl_comp, col_w, headers, data_comp)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================
    # 6. SYSTEM ARCHITECTURE & METHODOLOGY
    # ==========================
    add_styled_heading(doc, "5. System Architecture & Methodology", level=1)
    add_body_p(doc,
        "The project architecture integrates deterministic knowledge retrieval with state-of-the-art agentic reasoning, structured across four phases:")
    
    add_styled_heading(doc, "Phase 0: Ground-Truth Knowledge Pipeline (Milestone 0 - Fully Completed)", level=2)
    add_body_p(doc,
        "Raw official publications from the UNECE EUR-Lex portal (UN Regulation No. 155 OJ L 2025/5 Supplement 3), MITRE CAPEC View 2000 (v3.9), and MITRE CWE View 2000 (v4.20) are downloaded, hashed, and tracked in a provenance log. Custom parsers extract 67 authentic threats and 24 mitigations from UN R155 Annex 5, alongside 559 attack patterns and 938 weaknesses. Algorithmic mapping connects R155 threats to authentic CAPEC and CWE entries, generating a verified 50-entry library with original technical descriptions and concrete automotive attack examples.")

    add_styled_heading(doc, "Phase 1: Vector Storage & Contextual Retrieval (Milestone 1)", level=2)
    add_body_p(doc,
        "The verified JSON library is converted into semantic document chunks enriched with structured metadata (affected components, trust boundaries, communication protocols). ChromaDB indexes these documents using high-dimensional sentence embeddings. When a cybersecurity engineer queries the system about an ECU or interface, the retriever executes hybrid dense retrieval filtered by component metadata.")

    add_styled_heading(doc, "Phase 2: Agentic TARA Reasoning Engine (Milestone 2)", level=2)
    add_body_p(doc,
        "The reasoning agent ingests the retrieved threat context and applies the ISO/SAE 21434 methodology:", bold_prefix="ISO 21434 Workflow: ")
    add_bullet_item(doc, "Maps vehicle functions to cybersecurity properties (Confidentiality, Integrity, Availability).", bold_prefix="Asset & Damage Scenarios: ")
    add_bullet_item(doc, "Evaluates Elapsed Time, Specialist Expertise, Knowledge of Item, Window of Opportunity, and Equipment to score attack potential (Basic, Enhanced-Basic, Moderate, High).", bold_prefix="Attack Feasibility: ")
    add_bullet_item(doc, "Determines operational impact severity (Negligible, Moderate, Major, Severe) across Safety, Financial, Operational, and Privacy criteria.", bold_prefix="Impact Rating: ")
    add_bullet_item(doc, "Maps Feasibility and Impact onto the standardized ISO 21434 5x5 matrix to output Risk Value (1 to 5) and required cybersecurity goals.", bold_prefix="Risk Determination: ")

    add_styled_heading(doc, "Phase 3: Interactive Interface & Compliance Reporting (Milestone 3)", level=2)
    add_body_p(doc,
        "A responsive interface allows engineers to interactively query the vehicle risk profile, adjust threat parameters, and export audit-ready UN R155 Annex 5 compliance reports with clickable MITRE/EUR-Lex references for homologation authorities.")

    # ==========================
    # 7. HARDWARE & SOFTWARE SPECIFICATIONS
    # ==========================
    add_styled_heading(doc, "6. Hardware & Software Requirements", level=1)
    
    tbl_tech = doc.add_table(rows=1, cols=3)
    col_w_tech = [2.0, 2.2, 2.4]
    headers_tech = ["Technology / Tool", "Version / Specification", "Project Role"]
    data_tech = [
        ["Python", "3.13.x (Isolated Virtual Env)", "Core language runtime"],
        ["pdfplumber / pypdfium2", "v0.11.x / v5.14.x", "Official UN R155 regulatory document parsing"],
        ["BeautifulSoup4 / Requests", "v4.15.x / v2.34.x", "Automated MITRE dataset scraping and download"],
        ["Pydantic", "v2.14.x", "Strict schema validation and data integrity contracts"],
        ["pytest", "v9.1.x", "Automated regression testing and verification"],
        ["ChromaDB", "v0.5.x (Upcoming M1)", "High-speed embedded vector knowledge base"],
        ["Sentence-Transformers", "all-MiniLM-L6-v2 (Upcoming M1)", "Domain semantic embedding generation"],
        ["python-docx", "v1.2.x", "Automated audit documentation and synopsis generation"],
        ["Hardware Requirements", "Intel/AMD x64 or Apple Silicon, 8GB+ RAM", "Local lightweight execution without cloud dependency"]
    ]
    format_table(tbl_tech, col_w_tech, headers_tech, data_tech)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================
    # 8. CURRENT PROGRESS & MILESTONE 0 RESULTS
    # ==========================
    add_styled_heading(doc, "7. Current Progress & Milestone 0 Verification", level=1)
    add_body_p(doc,
        "Milestone 0 has been completed with 100% test passage and full compliance with all project criteria:")
    
    tbl_m0 = doc.add_table(rows=1, cols=3)
    col_w_m0 = [2.2, 1.8, 2.6]
    headers_m0 = ["Validation Requirement", "Target Metric", "Verified Result"]
    data_m0 = [
        ["Threat Library Entry Count", "40 to 60 Entries", "Exactly 50 entries (LIB-001 to LIB-050)"],
        ["Regulatory Category Coverage", "All 7 R155 Categories", "7 / 7 Categories represented (0 empty)"],
        ["Zero Invented IDs Rule", "100% Verifiable IDs", "0 hallucinated IDs; 100% exist in source CSVs"],
        ["Verbatim Name Match", "100% Verbatim Match", "All CAPEC and CWE names match official taxonomy"],
        ["Annex 5 Mitigation Mapping", "Part B & C References", "Directly mapped to M4, M7-M24 mitigations"],
        ["Component Architecture Alignment", "sample_vehicle.json", "All components and interfaces strictly validated"],
        ["Automated Test Suite", "Full test pass", "11 / 11 Pytest tests passed in 0.05 seconds"],
        ["Clickable Human Audit Report", "REVIEW.md with URLs", "Complete with official EUR-Lex & MITRE hyperlinks"]
    ]
    format_table(tbl_m0, col_w_m0, headers_m0, data_m0)
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================
    # 9. EXPECTED OUTCOMES & INDUSTRY IMPACT
    # ==========================
    add_styled_heading(doc, "8. Expected Outcomes & Industry Impact", level=1)
    add_body_p(doc,
        "The completion of this capstone project will deliver tangible value to the automotive engineering ecosystem:")
    add_bullet_item(doc, "Reduces initial threat analysis time from several weeks to under 30 minutes, freeing security specialists to focus on high-priority architectural hardening.", bold_prefix="Drastic Cycle Time Reduction: ")
    add_bullet_item(doc, "Eliminates cognitive variance and subjective bias by grounding every risk assessment in standardized ISO 21434 attack feasibility formulas.", bold_prefix="Repeatable, Objective Assessments: ")
    add_bullet_item(doc, "Produces direct, auditable compliance traceability matrices required by Technical Services and National Approval Authorities (e.g., KBA, VCA, ARAI) for vehicle type approval.", bold_prefix="Audit Readiness for Type Approval: ")
    add_bullet_item(doc, "Demonstrates a state-of-the-art methodology for deploying LLMs in safety-critical domains where hallucination tolerance is zero.", bold_prefix="Reference Architecture for Trustworthy AI: ")

    # ==========================
    # 10. REFERENCES & STANDARDS
    # ==========================
    add_styled_heading(doc, "9. References & Regulatory Standards", level=1)
    add_bullet_item(doc, "UNECE, 'UN Regulation No. 155: Uniform provisions concerning the approval of vehicles with regards to cyber security and cyber security management system', Official Journal of the European Union, OJ L 2025/5.", bold_prefix="[1] ")
    add_bullet_item(doc, "ISO/SAE, 'ISO/SAE 21434:2021 Road vehicles — Cybersecurity engineering', International Organization for Standardization / SAE International, 2021.", bold_prefix="[2] ")
    add_bullet_item(doc, "MITRE Corporation, 'Common Attack Pattern Enumeration and Classification (CAPEC™) Version 3.9', Comprehensive Dictionary View 2000, 2024.", bold_prefix="[3] ")
    add_bullet_item(doc, "MITRE Corporation, 'Common Weakness Enumeration (CWE™) Version 4.20', Comprehensive View 2000, 2024.", bold_prefix="[4] ")
    add_bullet_item(doc, "UNECE, 'UN Regulation No. 156: Software update and software update management system', United Nations Economic Commission for Europe, 2021.", bold_prefix="[5] ")

    # ==========================
    # 10. SYSTEM VISUAL VERIFICATION & SCREENSHOTS
    # ==========================
    add_styled_heading(doc, "10. System Visual Verification & Dashboard Screenshots", level=1)
    add_body_p(doc,
        "The project includes an interactive web-based dashboard (accessible locally at http://127.0.0.1:8080) for engineering reviews, architecture inspection, threat browsing, and ISO/SAE 21434 risk simulation. Below are official screenshots of the running system:")

    screenshots_dir = os.path.join("docs", "screenshots")
    screenshot_items = [
        ("01_dashboard_overview.png", "Figure 1: Executive KPI Dashboard & Target Vehicle E/E Architecture View"),
        ("02_threat_library_explorer.png", "Figure 2: Verified Threat Library Explorer (50 entries with CAPEC/CWE/R155 Badges)"),
        ("03_iso21434_risk_simulator.png", "Figure 3: Interactive ISO/SAE 21434 Attack Feasibility & SFOP Impact Parameter Simulator"),
        ("04_tara_5x5_risk_matrix.png", "Figure 4: Realtime 5x5 ISO 21434 Risk Determination Matrix & R155 Mitigation Recommendation"),
        ("05_compliance_audit_matrix.png", "Figure 5: Homologation Compliance & Audit Trail Matrix with Clickable MITRE / EUR-Lex URLs")
    ]

    for filename, caption in screenshot_items:
        img_path = os.path.join(screenshots_dir, filename)
        if os.path.exists(img_path):
            doc.add_picture(img_path, width=Inches(6.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(3)
            p_cap.paragraph_format.space_after = Pt(12)
            r_cap = p_cap.add_run(caption)
            r_cap.font.name = "Calibri"
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = COLOR_MUTED

    # Save
    doc.save(OUTPUT_DOCX)
    print(f"Project synopsis Word Document successfully saved to: {OUTPUT_DOCX}")

if __name__ == "__main__":
    generate_synopsis()
