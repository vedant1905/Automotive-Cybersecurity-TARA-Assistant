# Automotive Cybersecurity TARA Assistant
> **AI-Powered Threat Analysis & Risk Assessment (TARA) Platform Grounded in UN R155 Annex 5, ISO/SAE 21434:2021, and MITRE CAPEC/CWE Taxonomy**

[![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Regulation](https://img.shields.io/badge/Compliance-UN%20R155%20Annex%205-green.svg)](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf)
[![Standard](https://img.shields.io/badge/Standard-ISO%2FSAE%2021434%3A2021-blue.svg)](https://www.iso.org/standard/70918.html)
[![Zero Hallucinations](https://img.shields.io/badge/Zero%20Hallucinations-Enforced-emerald.svg)](#)
[![Tests](https://img.shields.io/badge/Tests-11%20Passed%20(0.08s)-brightgreen.svg)](#)

---

## 📌 Executive Overview

The **Automotive Cybersecurity TARA Assistant** is an engineering intelligence platform developed for the **Tata TechPulse Capstone**. It automates and streamlines Threat Analysis and Risk Assessment (TARA) for modern connected vehicles under **UN Regulation No. 155 (Annex 5)** and **ISO/SAE 21434:2021**.

To prevent the hazardous failure modes of commercial generative AI—where models regularly hallucinate non-existent CVE, CWE, or CAPEC identifiers—this system enforces a strict **Zero Hallucination Policy**. Every threat, attack pattern, weakness classification, and mitigation trace is strictly grounded in authenticated source data extracted directly from official UNECE EUR-Lex regulations and MITRE repositories.

---

## 🚗 Target Connected Vehicle Architecture Scope

The system evaluates a reference Connected and Automated Passenger Vehicle architecture defined in [`data/system/sample_vehicle.json`](data/system/sample_vehicle.json):

```
┌────────────────────────────────────────────────────────────────────────┐
│               CLOUD INFRASTRUCTURE (REMOTE TIER)                       │
│    [Cloud OTA Backend Server & Fleet Telematics API (REST/TLS 1.3)]    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ 4G/5G Cellular / TLS 1.3
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          UNTRUSTED WIRELESS PERIMETER (EXTERNAL EDGE DOMAIN)           │
│   ┌────────────────────────────────┐   ┌───────────────────────────┐   │
│   │ Telematics Control Unit (TCU)  │   │ In-Vehicle Infotainment   │   │
│   │ • 4G/5G Cellular, BLE, Wi-Fi   │   │ • Linux/Android, USB, BT  │   │
│   │ • GNSS Positioning, eCall      │   │ • Smartphone Projection   │   │
│   └───────────────┬────────────────┘   └─────────────┬─────────────┘   │
└───────────────────┼──────────────────────────────────┼─────────────────┘
                    │ 100BASE-T1 & CAN                 │ Automotive Ethernet
                    ▼                                  ▼
┌────────────────────────────────────────────────────────────────────────┐
│           SECURITY GATEWAY DEMARCATION & ISOLATION ZONE                │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ Central Security Gateway (CGW)                                 │   │
│   │ • Domain Firewall & Filtering  • SecOC (AUTOSAR) Verification  │   │
│   │ • Hardware Security Module     • Inter-Domain Protocol Routing │   │
│   └────────────────────────────────┬───────────────────────────────┘   │
└────────────────────────────────────┼───────────────────────────────────┘
                    ▲                │ High-Speed CAN-FD + SecOC MACs
                    │ CAN 2.0B / UDS │
┌───────────────────┴────────────────┼───────────────────────────────────┐
│ PHYSICAL MAINTENANCE               ▼                                   │
│ [OBD-II 16-Pin Diagnostic Port]    [High-Trust Safety Domain]          │
│ • Dealership Flash / Diagnostics   • Powertrain ECU (Torque / Throttle)│
│ • UDS (ISO 14229) Seed-Key Access  • Brake ECU (ESC / ABS Actuation)   │
└────────────────────────────────────────────────────────────────────────┘
```

| Component | Trust Boundary Zone | Interfaces | Critical Functions |
| :--- | :--- | :--- | :--- |
| **Telematics Control Unit (TCU)** | Wireless Edge Domain | 4G/5G, BLE, Wi-Fi, GNSS, CAN, Ethernet | Remote OTA reception, telematics dispatch, eCall |
| **Central Security Gateway (CGW)** | Demarcation Gateway | CAN-FD, Automotive Ethernet, OBD-II | Firewall filtering, domain separation, SecOC MAC verification |
| **Infotainment Head Unit (IVI)** | Infotainment Domain | USB, Wi-Fi Hotspot, Bluetooth, Ethernet | Media rendering, smartphone integration, user apps |
| **OBD-II Diagnostic Port** | Physical Maintenance | 16-Pin Connector, CAN 2.0B, UDS (ISO 14229) | Dealership diagnostics, ECU re-flashing |
| **Powertrain Control Module (PCM)** | Safety Domain (ASIL-D) | High-Speed CAN-FD Bus | Electronic throttle actuation, motor/engine torque control |
| **Brake System ECU (ESC/ABS)** | Safety Domain (ASIL-D) | High-Speed CAN-FD Bus | Anti-lock braking, electronic stability control, AEB |
| **Cloud OTA Backend & API** | Cloud Remote Tier | Internet / HTTPS REST API, TLS 1.3 | Firmware signing, campaign distribution, fleet telemetry |

---

## ⚡ Key Features & Capabilities

1. **50 Verified Ground-Truth Threats**:
   - Comprehensive coverage across all 7 categories of UN R155 Annex 5 Part A.
   - Programmatically linked to authentic MITRE CAPEC attack patterns, MITRE CWE weaknesses, and Annex 5 Part B/C mitigations.
   - **Zero Invented IDs**: 100% cross-referenced against authoritative EUR-Lex and MITRE CSV sources.
2. **Interactive Web Engineering Dashboard**:
   - Runs 100% locally on standard workstation hardware via Python HTTP server.
   - Interactive E/E network topology demarcation visualizer.
   - Real-time threat library explorer with instant keyword, category, and confidence filters.
   - **ISO/SAE 21434 5×5 Risk Matrix Simulator**: Dynamic Attack Feasibility Rating (AFR) calculation and SFOP impact evaluation.
   - **UN R155 Compliance & Mitigation Audit Matrix**: Audit-ready mapping from threats to approved engineering mitigations.
3. **Automated CI/CD Verification Harness**:
   - Continuous regression testing with 11 automated unit tests executing in under 0.1 seconds.

---

## 🚀 Quickstart & How to Run

### 1. Prerequisites
- Python 3.10+ (Recommended: Python 3.13)
- Git

### 2. Installation
```powershell
# Clone the repository
git clone https://github.com/vedant1905/Automotive-Cybersecurity-TARA-Assistant.git
cd Automotive-Cybersecurity-TARA-Assistant

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Web Engineering Dashboard
```powershell
python scripts/serve_dashboard.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:8081
```

### 4. Run Automated Unit Tests
```powershell
pytest -v tests/test_library_validation.py
```
All 11 verification tests will execute with a 100% pass rate.

---

## 🔬 ISO/SAE 21434 Quantitative Risk Formulation

The platform implements the standard's Attack Feasibility Rating (AFR) parameter formula:

$$\text{AFR} = \text{Elapsed Time} + \text{Specialist Expertise} + \text{Knowledge of Item} + \text{Window of Opportunity} + \text{Equipment}$$

- **Feasibility Thresholds**: High (0–13 pts), Medium (14–19 pts), Low (20–24 pts), Very Low ($\ge 25$ pts).
- **SFOP Impact Scoring**: $\max(\text{Safety}, \text{Financial}, \text{Operational}, \text{Privacy})$ from Negligible (0) to Severe (3).
- **5×5 Matrix Lookup**: Determines standard Risk Values ($RV \in [1, 5]$).

---

## 📁 Repository Structure

```text
├── configs/
│   ├── model_prompts_config.yaml     # LLM hyperparameters & system prompt guardrails
│   └── model_prompts_config.json     # JSON representation for frontend API
├── data/
│   ├── library/
│   │   ├── threat_library.json       # 50 verified ground-truth threats (LIB-001..050)
│   │   └── REVIEW.md                 # Human audit review log for flagged mappings
│   ├── processed/
│   │   ├── r155_threats.csv          # 67 extracted threats from Annex 5 Part A
│   │   ├── r155_mitigations.csv      # 24 extracted mitigations from Annex 5 Parts B/C
│   │   ├── capec.csv                 # Parsed MITRE CAPEC View 2000 attack patterns
│   │   └── cwe.csv                   # Parsed MITRE CWE View 2000 weakness enumerations
│   ├── raw/
│   │   └── SOURCES.md                # Cryptographic provenance log (SHA-256 hashes)
│   └── system/
│       └── sample_vehicle.json       # Reference CAV E/E architecture model
├── scripts/
│   ├── 01_download_sources.py        # Automated ingestion & cryptographic auditing
│   ├── 02_extract_r155.py            # PDF table extraction of UN R155 Annex 5
│   ├── 03_parse_capec_cwe.py         # Parsing of MITRE taxonomies
│   ├── 04_map_threats.py             # Multi-standard semantic linkage engine
│   ├── 05_build_threat_library.py    # Zero-hallucination synthesis engine
│   ├── 06_generate_review.py         # Human audit log generator
│   ├── serve_dashboard.py            # Local HTTP dashboard server with no-cache headers
│   └── validate_library.py           # Programmatic schema validation runner
├── tests/
│   └── test_library_validation.py    # 11 unit tests for CI/CD regression testing
├── web/
│   ├── index.html                    # Single-page enterprise dashboard interface
│   ├── style.css                     # Corporate light-theme styling system
│   └── app.js                        # Frontend state, filters, and 5x5 simulator logic
├── requirements.txt                  # Python project dependencies
├── .gitignore                        # Git ignore rules (excludes docs/, .venv, etc.)
└── README.md                         # Project documentation
```

---

## 📜 Regulatory Standards & Provenance Citations
- **UNECE UN Regulation No. 155**: Cyber security and cyber security management system, Annex 5. [EUR-Lex Document 32025R0005](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf)
- **ISO/SAE 21434:2021**: Road vehicles — Cybersecurity engineering. [ISO Catalog](https://www.iso.org/standard/70918.html)
- **MITRE CAPEC™**: Common Attack Pattern Enumeration and Classification, View 2000. [MITRE CAPEC](https://capec.mitre.org/)
- **MITRE CWE™**: Common Weakness Enumeration, View 2000. [MITRE CWE](https://cwe.mitre.org/)

---
*Developed for the Tata TechPulse Capstone Initiative.*
