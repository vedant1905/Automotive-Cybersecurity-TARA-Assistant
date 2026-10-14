# Automotive Cybersecurity Threat Library - Human Review Report

This report audits the verified Threat Library (`data/library/threat_library.json`) for the Automotive Cybersecurity TARA Assistant.
All entries below include direct official links to MITRE CAPEC, MITRE CWE, and the official EUR-Lex publication of UN Regulation No. 155.

## 1. Summary Statistics

- **Total Library Entries**: 50
- **Entries with High Confidence**: 42
- **Entries Flagged for Human Review**: 8
- **Audit Sampled High-Confidence Entries**: 10
- **Total Audited Entries in this Report**: 18

---

## 2. Flagged Entries Requiring Human Review (`needs_human_review = true`)

The following entries have `medium` or `low` mapping confidence, or represent specialized domain concepts (e.g., RF jamming, supply chain hardware trojans, or multi-tenant storage leakage) that warrant expert validation:

### [LIB-006] Multi-Tenant Cloud Storage Misconfiguration and Data Leakage
- **UN R155 Threat ID**: [3.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.1 Threats regarding back-end servers related to vehicles in the field`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: OTA Backend Server & Mobile App API
- **Affected Interfaces**: Internet / REST API
- **Technical Description**: Misconfigured access controls or storage bucket permissions on third-party cloud hosting infrastructure expose stored automotive telemetry. Attackers or unauthorized cloud tenants can enumerate unsecured object storage containing vehicle crash logs and diagnostic dumps. This failure in multi-tenant data isolation leads to widespread disclosure of proprietary system telemetry.
- **Concrete Attack Scenario**: *"An unsecured Amazon S3 cloud bucket containing unencrypted vehicle sensor telemetry and camera snapshots is indexed by open-source intelligence scanners."*
- **MITRE CAPEC**: [CAPEC-546: Incomplete Data Deletion in a Multi-Tenant Environment](https://capec.mitre.org/data/definitions/546.html)
- **MITRE CWE**: [CWE-284: Improper Access Control](https://cwe.mitre.org/data/definitions/284.html)
- **UN R155 Mitigations**: `M8` (Confidential data transmitted to or from the vehicle shall be protected)

### [LIB-009] Sybil Attack Fabricating Phantom Traffic Nodes
- **UN R155 Threat ID**: [4.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: Telematics Control Unit (TCU)
- **Affected Interfaces**: Cellular, Wi-Fi
- **Technical Description**: An adversary creates multiple fake identities across wireless communication channels to simulate the presence of phantom vehicles on the roadway. The vehicle's external communication stack processes these fictitious node transmissions as a congested traffic stream. This can mislead routing algorithms and trigger unwarranted vehicle safety responses.
- **Concrete Attack Scenario**: *"A roadside transmitter broadcasts dozens of distinct cooperative awareness messages simulating a major traffic jam, forcing connected vehicles to brake or reroute."*
- **MITRE CAPEC**: [CAPEC-151: Identity Spoofing](https://capec.mitre.org/data/definitions/151.html)
- **MITRE CWE**: [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-013] Malicious Erasure of Safety Calibration Data via Diagnostic Bus
- **UN R155 Threat ID**: [5.4](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: Central Gateway (CGW), Brake ECU
- **Affected Interfaces**: CAN
- **Technical Description**: Adversaries exploit diagnostic communication channels to invoke flash erase or parameter reset routines on target electronic control units. Erasing stored cryptographic certificates, fault tables, or sensor calibrations forces the target subsystem into an unrecoverable fail-safe or limp-home mode. This disrupts continuous vehicle availability and safety operations.
- **Concrete Attack Scenario**: *"An attacker transmits diagnostic session commands that execute an unauthenticated routine erase on the brake ECU flash storage, wiping essential brake balance calibrations."*
- **MITRE CAPEC**: [CAPEC-153: Input Data Manipulation](https://capec.mitre.org/data/definitions/153.html)
- **MITRE CWE**: [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-029] Technician Violation of Diagnostic Security Protocols
- **UN R155 Threat ID**: [15.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.4 Threats to vehicles regarding unintended human actions facilitating a cyber-attack`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: OBD-II Diagnostic Port, Central Gateway (CGW)
- **Affected Interfaces**: UDS over CAN
- **Technical Description**: Service technicians or maintenance personnel fail to adhere to established security protocols, such as using shared diagnostic credentials or leaving debug modes active. These procedural lapses expose sensitive vehicle diagnostic interfaces to unauthorized manipulation. Failure to maintain operational discipline creates easily exploitable entry points for malicious actors.
- **Concrete Attack Scenario**: *"A workshop mechanic leaves a diagnostic gateway unlocked with static factory security keys plugged in overnight, leaving the vehicle bus accessible to passersby."*
- **MITRE CAPEC**: [CAPEC-180: Exploiting Incorrectly Configured Access Control Security Levels](https://capec.mitre.org/data/definitions/180.html)
- **MITRE CWE**: [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html)
- **UN R155 Mitigations**: `M18` (Measures shall be implemented for defining and controlling user roles and access rights); `M19` (Security awareness and training shall be provided)

### [LIB-032] Radio Frequency Jamming of Short-Range Vehicle Wireless Links
- **UN R155 Threat ID**: [16.3](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.5 Threats to vehicles regarding their external connectivity and connections`
- **Mapping Confidence**: `LOW`
- **Affected Components**: Telematics Control Unit (TCU), Infotainment Unit (IVI)
- **Affected Interfaces**: Wi-Fi, Bluetooth
- **Technical Description**: Adversaries deploy RF jamming equipment operating on 2.4 GHz and 5 GHz bands to disrupt Bluetooth, Wi-Fi, and short-range sensor transmissions. Saturating these communication bands causes sensor timeouts, drops tire pressure monitoring connections, and disconnects driver smartphone interfaces. This degrades peripheral situational awareness and driver communication channels.
- **Concrete Attack Scenario**: *"A broadband radio jammer blocks Bluetooth and Wi-Fi channels, severing communications between wireless tire pressure sensors and the central gateway."*
- **MITRE CAPEC**: [CAPEC-603: Blockage](https://capec.mitre.org/data/definitions/603.html)
- **MITRE CWE**: *(None / Hardware or procedural failure)*
- **UN R155 Mitigations**: `M21` (Cryptographic controls shall be applied to protect communication confidentiality and integrity)

### [LIB-040] Tampering with Regulatory Monitoring and Odometer Telemetry
- **UN R155 Threat ID**: [20.3](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.6 Potential targets of, or motivations for, an attack on vehicles`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: Telematics Control Unit (TCU), Central Gateway (CGW)
- **Affected Interfaces**: CAN, Cellular
- **Technical Description**: Adversaries block, modify, or inject falsified telemetry frames to circumvent vehicle operational monitoring and odometer recording systems. Altering mileage records, run-time counters, or emissions monitoring data deceives regulatory compliance audits and vehicle tracking systems. This enables fraudulent vehicle resale or evasion of regulatory inspections.
- **Concrete Attack Scenario**: *"A microcontroller spliced into the instrument cluster CAN bus filters and modifies odometer pulse messages to prevent mileage accumulation."*
- **MITRE CAPEC**: [CAPEC-180: Exploiting Incorrectly Configured Access Control Security Levels](https://capec.mitre.org/data/definitions/180.html)
- **MITRE CWE**: [CWE-732: Incorrect Permission Assignment for Critical Resource](https://cwe.mitre.org/data/definitions/732.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-041] Unauthorized Manipulation and Clearing of Diagnostic Trouble Codes
- **UN R155 Threat ID**: [20.5](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.6 Potential targets of, or motivations for, an attack on vehicles`
- **Mapping Confidence**: `MEDIUM`
- **Affected Components**: Central Gateway (CGW), OBD-II Diagnostic Port
- **Affected Interfaces**: UDS over CAN, CAN
- **Technical Description**: Adversaries execute unauthorized UDS diagnostic services to alter or erase Diagnostic Trouble Codes (DTCs) and freeze-frame sensor data. Suppressing active fault warnings prevents drivers and service technicians from detecting critical subsystem failures or security tampering. This conceals ongoing component degradation and safety-critical malfunctions.
- **Concrete Attack Scenario**: *"An adversary issues an unauthenticated UDS ClearDiagnosticInformation command to wipe airbag system fault records prior to vehicle safety inspection."*
- **MITRE CAPEC**: [CAPEC-153: Input Data Manipulation](https://capec.mitre.org/data/definitions/153.html)
- **MITRE CWE**: [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-047] Hardware Supply-Chain Trojan Implanted in Vehicle Controller
- **UN R155 Threat ID**: [27.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened`
- **Mapping Confidence**: `LOW`
- **Affected Components**: Central Gateway (CGW), Powertrain ECU, Brake ECU
- **Affected Interfaces**: CAN, Automotive Ethernet
- **Technical Description**: Compromised third-party hardware components or malicious design modifications are introduced into ECU hardware during manufacturing and assembly. The embedded hardware trojan activates under specific bus conditions or timer triggers, providing covert hardware backdoors. This circumvents all software-level security controls and runtime integrity verifications.
- **Concrete Attack Scenario**: *"A counterfeit microcontroller containing a hidden silicon backdoor is installed into the central gateway during assembly, allowing unauthorized hardware bus access."*
- **MITRE CAPEC**: [CAPEC-438: Modification During Manufacture](https://capec.mitre.org/data/definitions/438.html)
- **MITRE CWE**: *(None / Hardware or procedural failure)*
- **UN R155 Mitigations**: `M23` (Security testing and verification shall be performed during development)

---

## 3. Audited High-Confidence Sample Entries (10 Random Entries)

Representative cross-section of high-confidence entries across different vehicle domains:

### [LIB-049] Exploitation of Active Hardware Debug Interfaces in Production Vehicles
- **UN R155 Threat ID**: [28.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.7 Potential vulnerabilities that could be exploited if not sufficiently protected or hardened`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Central Gateway (CGW), OBD-II Diagnostic Port
- **Affected Interfaces**: UDS over CAN, CAN
- **Technical Description**: Hardware development artifacts such as active JTAG ports, serial UART consoles, or default engineering test accounts are left enabled on production ECUs. Attackers connect physical debugging probes to read raw memory, set hardware breakpoints, and bypass software security restrictions. This provides unrestricted low-level access to ECU silicon.
- **Concrete Attack Scenario**: *"An adversary connects a JTAG hardware debugger to unpopulated test pads on the TCU printed circuit board, dumping internal flash memory and bypassing secure boot."*
- **MITRE CAPEC**: [CAPEC-190: Reverse Engineer an Executable to Expose Assumed Hidden Functionality](https://capec.mitre.org/data/definitions/190.html)
- **MITRE CWE**: [CWE-912: Hidden Functionality](https://cwe.mitre.org/data/definitions/912.html)
- **UN R155 Mitigations**: `M23` (Security testing and verification shall be performed during development)

### [LIB-010] Arbitrary Code Injection into Cellular Telematics Stream
- **UN R155 Threat ID**: [5.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Central Gateway (CGW), Powertrain ECU, Brake ECU
- **Affected Interfaces**: CAN, Automotive Ethernet
- **Technical Description**: Attackers inject malicious binary sequences into open communication streams between the vehicle telematics module and backend networks. If payload integrity and stream boundaries are not strictly validated, the telematics controller executes injected machine instructions. This grants the attacker remote execution capabilities inside the wireless edge domain.
- **Concrete Attack Scenario**: *"An attacker injects shellcode into an unencrypted cellular telemetry TCP stream, triggering a stack buffer overflow that executes arbitrary code on the TCU."*
- **MITRE CAPEC**: [CAPEC-242: Code Injection](https://capec.mitre.org/data/definitions/242.html)
- **MITRE CWE**: [CWE-94: Improper Control of Generation of Code ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-002] Remote Exploitation of Cloud Telematics API Server
- **UN R155 Threat ID**: [1.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.1 Threats regarding back-end servers related to vehicles in the field`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: OTA Backend Server & Mobile App API
- **Affected Interfaces**: Internet / REST API
- **Technical Description**: External adversaries exploit software vulnerabilities such as unpatched services or web application flaws in the OEM cloud telematics backend. By breaching the internet-facing server boundary, the attacker establishes persistence within the fleet orchestration infrastructure. This provides an external pivot point to interact directly with connected vehicles in the field.
- **Concrete Attack Scenario**: *"An external attacker executes a SQL injection exploit against the fleet telematics REST portal to extract authentication tokens for connected vehicle sessions."*
- **MITRE CAPEC**: [CAPEC-66: SQL Injection](https://capec.mitre.org/data/definitions/66.html), [CAPEC-115: Authentication Bypass](https://capec.mitre.org/data/definitions/115.html)
- **MITRE CWE**: [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html), [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- **UN R155 Mitigations**: `M4` (The vehicle shall be capable of updating)

### [LIB-021] Local Privilege Escalation to Root on Telematics OS
- **UN R155 Threat ID**: [9.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Central Gateway (CGW), Telematics Control Unit (TCU)
- **Affected Interfaces**: Automotive Ethernet, CAN
- **Technical Description**: An adversary with limited execution privileges on the telematics control unit exploits local operating system vulnerabilities to attain superuser or root permissions. Gaining administrative control circumvents application sandbox constraints and access control policies. This enables the adversary to manipulate physical bus transceivers and access raw peripheral memory.
- **Concrete Attack Scenario**: *"A standard user process on the Linux-based TCU exploits an unpatched kernel vulnerability to escalate privileges to root, gaining unfettered access to the internal CAN interface."*
- **MITRE CAPEC**: [CAPEC-233: Privilege Escalation](https://capec.mitre.org/data/definitions/233.html)
- **MITRE CWE**: [CWE-269: Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html)
- **UN R155 Mitigations**: `M9` (Measures to prevent and detect unauthorized access shall be employed)

### [LIB-019] Unauthorized Extraction of Driver Records from Infotainment Storage
- **UN R155 Threat ID**: [7.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Central Gateway (CGW), Infotainment Unit (IVI)
- **Affected Interfaces**: Automotive Ethernet, USB
- **Technical Description**: Attackers exploit permissive file system permissions or local debugging services on the infotainment head unit to access stored passenger data. Unprotected local storage exposes call logs, navigation histories, paired phone contacts, and stored credentials. This breach of local data privacy exposes sensitive owner information to unauthorized actors.
- **Concrete Attack Scenario**: *"A malicious script running on the infotainment operating system reads stored navigation destination caches and synchronized Bluetooth smartphone address books."*
- **MITRE CAPEC**: [CAPEC-122: Privilege Abuse](https://capec.mitre.org/data/definitions/122.html)
- **MITRE CWE**: [CWE-269: Improper Privilege Management](https://cwe.mitre.org/data/definitions/269.html)
- **UN R155 Mitigations**: `M12` (Confidential data transmitted to or from the vehicle shall be protected)

### [LIB-018] Passive Eavesdropping and RF Radiation Sniffing on Vehicle Buses
- **UN R155 Threat ID**: [7.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Telematics Control Unit (TCU), Central Gateway (CGW)
- **Affected Interfaces**: Cellular, Automotive Ethernet, CAN
- **Technical Description**: Adversaries deploy packet sniffers or radio frequency receivers to capture unencrypted data traversing vehicle buses and wireless links. By monitoring cleartext communications, the attacker extracts diagnostic trouble codes, vehicle operational telemetry, and proprietary message identifiers. This intelligence is leveraged to reverse engineer communication protocols and design targeted exploits.
- **Concrete Attack Scenario**: *"An attacker clips an inductive sensor onto the unshielded CAN bus harness to passively record torque commands and vehicle speed signals in cleartext."*
- **MITRE CAPEC**: [CAPEC-157: Sniffing Attacks](https://capec.mitre.org/data/definitions/157.html), [CAPEC-651: Eavesdropping](https://capec.mitre.org/data/definitions/651.html)
- **MITRE CWE**: [CWE-311: Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html), [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
- **UN R155 Mitigations**: `M12` (Confidential data transmitted to or from the vehicle shall be protected)

### [LIB-011] Tampering with In-Transit In-Vehicle Bus Communication
- **UN R155 Threat ID**: [5.2](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Central Gateway (CGW), Powertrain ECU, Brake ECU
- **Affected Interfaces**: CAN
- **Technical Description**: Adversaries manipulate frame payloads or control parameters while messages transit vehicle gateways and network buses. By modifying critical signal values such as speed, steering angle, or sensor telemetry, the attacker alters vehicle operational behavior. Lack of message authentication enables this unauthorized alteration of in-flight vehicle data.
- **Concrete Attack Scenario**: *"An attacker modifies vehicle speed signals inside transit CAN frames from the gateway, deceiving the instrument cluster and advanced driver-assistance controllers."*
- **MITRE CAPEC**: [CAPEC-153: Input Data Manipulation](https://capec.mitre.org/data/definitions/153.html)
- **MITRE CWE**: [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-008] V2X and GNSS Positioning Message Spoofing
- **UN R155 Threat ID**: [4.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.2 Threats to vehicles regarding their communication channels`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Telematics Control Unit (TCU), Central Gateway (CGW)
- **Affected Interfaces**: Cellular, Automotive Ethernet
- **Technical Description**: Attackers broadcast falsified wireless messages mimicking legitimate road infrastructure, neighboring vehicles, or satellite navigation signals. The vehicle telematics or infotainment unit accepts these unauthenticated transmissions and propagates corrupted state data to internal control units. This can cause automated driver-assistance modules to react to non-existent road hazards.
- **Concrete Attack Scenario**: *"An adversary uses a software-defined radio to transmit spoofed GNSS coordinate signals, causing the vehicle navigation and telematics unit to report an incorrect geographical position."*
- **MITRE CAPEC**: [CAPEC-151: Identity Spoofing](https://capec.mitre.org/data/definitions/151.html), [CAPEC-148: Content Spoofing](https://capec.mitre.org/data/definitions/148.html)
- **MITRE CWE**: [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html), [CWE-345: Insufficient Verification of Data Authenticity](https://cwe.mitre.org/data/definitions/345.html)
- **UN R155 Mitigations**: *(No direct Part B/C table mapping)*

### [LIB-007] Web Application Breach of Fleet Management Database
- **UN R155 Threat ID**: [3.3](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.1 Threats regarding back-end servers related to vehicles in the field`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: OTA Backend Server & Mobile App API
- **Affected Interfaces**: Internet / REST API
- **Technical Description**: Adversaries leverage web-facing application vulnerabilities to bypass authentication and query production vehicle databases directly. Unauthorized queries reveal vehicle cryptographic seeds, owner identities, and telematics configurations. Compromising this persistent storage layer enables downstream targeted attacks against individual vehicles.
- **Concrete Attack Scenario**: *"An attacker exploits an authentication bypass vulnerability in the fleet management web portal to dump customer account credentials and paired vehicle VIN numbers."*
- **MITRE CAPEC**: [CAPEC-66: SQL Injection](https://capec.mitre.org/data/definitions/66.html), [CAPEC-115: Authentication Bypass](https://capec.mitre.org/data/definitions/115.html)
- **MITRE CWE**: [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html), [CWE-287: Improper Authentication](https://cwe.mitre.org/data/definitions/287.html)
- **UN R155 Mitigations**: `M4` (The vehicle shall be capable of updating)

### [LIB-033] Compromise of Infotainment OS via Vulnerable Third-Party Apps
- **UN R155 Threat ID**: [17.1](https://eur-lex.europa.eu/eli/reg/2025/5/oj/eng/pdf) (Annex 5 Part A)
- **Category**: `4.3.5 Threats to vehicles regarding their external connectivity and connections`
- **Mapping Confidence**: `HIGH`
- **Affected Components**: Infotainment Unit (IVI)
- **Affected Interfaces**: Wi-Fi, USB
- **Technical Description**: Vulnerabilities in third-party media applications or browser engines running on the infotainment operating system are exploited by external adversaries. Attackers leverage malformed media files or malicious web content to escape application sandboxes and execute code within the head unit. This turns user-installed software into an initial beachhead within the vehicle network.
- **Concrete Attack Scenario**: *"A malicious audio file played through a vulnerable third-party streaming app triggers a heap overflow that gives an attacker a command shell on the IVI system."*
- **MITRE CAPEC**: [CAPEC-242: Code Injection](https://capec.mitre.org/data/definitions/242.html), [CAPEC-100: Overflow Buffers](https://capec.mitre.org/data/definitions/100.html)
- **MITRE CWE**: [CWE-94: Improper Control of Generation of Code ('Code Injection')](https://cwe.mitre.org/data/definitions/94.html), [CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')](https://cwe.mitre.org/data/definitions/120.html)
- **UN R155 Mitigations**: `M7` (Access control techniques and designs shall be applied to protect system data/code. Example Security Controls can be found in OWASP); `M24` (Vulnerability management and incident response processes shall be implemented)

---

## 4. Verification Check Instructions
To independently verify this Threat Library at any time, execute the following commands in the virtual environment:
```powershell
.\.venv\Scripts\python.exe scripts\validate_library.py
.\.venv\Scripts\pytest.exe -v tests/test_library_validation.py
```
