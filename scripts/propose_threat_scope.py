import os
import csv
import json

THREATS_CSV = os.path.join("data", "processed", "r155_threats.csv")
VEHICLE_JSON = os.path.join("data", "system", "sample_vehicle.json")

# Selected 50 high-relevance threats across all 7 categories
SELECTION = [
    # 4.3.1 Threats regarding back-end servers (7 threats)
    {
        "r155_threat_id": "1.1",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    {
        "r155_threat_id": "1.2",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    {
        "r155_threat_id": "1.3",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    {
        "r155_threat_id": "2.1",
        "affected_components": ["OTA Backend Server & Mobile App API", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular", "Internet / REST API"]
    },
    {
        "r155_threat_id": "3.1",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    {
        "r155_threat_id": "3.2",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    {
        "r155_threat_id": "3.3",
        "affected_components": ["OTA Backend Server & Mobile App API"],
        "affected_interfaces": ["Internet / REST API"]
    },
    # 4.3.2 Threats to vehicles regarding communication channels (15 threats)
    {
        "r155_threat_id": "4.1",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "4.2",
        "affected_components": ["Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular", "Wi-Fi"]
    },
    {
        "r155_threat_id": "5.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "5.2",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "5.3",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "5.4",
        "affected_components": ["Central Gateway (CGW)", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "5.5",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "6.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "6.2",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "6.3",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "7.1",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet", "CAN"]
    },
    {
        "r155_threat_id": "7.2",
        "affected_components": ["Central Gateway (CGW)", "Infotainment Unit (IVI)"],
        "affected_interfaces": ["Automotive Ethernet", "USB"]
    },
    {
        "r155_threat_id": "8.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "9.1",
        "affected_components": ["Central Gateway (CGW)", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Automotive Ethernet", "CAN"]
    },
    {
        "r155_threat_id": "11.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    # 4.3.3 Threats regarding update process (5 threats)
    {
        "r155_threat_id": "12.1",
        "affected_components": ["OTA Backend Server & Mobile App API", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "12.2",
        "affected_components": ["Central Gateway (CGW)", "OBD-II Diagnostic Port"],
        "affected_interfaces": ["UDS over CAN"]
    },
    {
        "r155_threat_id": "12.3",
        "affected_components": ["OTA Backend Server & Mobile App API", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "12.4",
        "affected_components": ["OTA Backend Server & Mobile App API", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Internet / REST API", "Cellular"]
    },
    {
        "r155_threat_id": "13.1",
        "affected_components": ["OTA Backend Server & Mobile App API", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular", "Internet / REST API"]
    },
    # 4.3.4 Threats regarding unintended human actions (2 threats)
    {
        "r155_threat_id": "15.1",
        "affected_components": ["Infotainment Unit (IVI)", "OBD-II Diagnostic Port"],
        "affected_interfaces": ["USB", "UDS over CAN"]
    },
    {
        "r155_threat_id": "15.2",
        "affected_components": ["OBD-II Diagnostic Port", "Central Gateway (CGW)"],
        "affected_interfaces": ["UDS over CAN"]
    },
    # 4.3.5 Threats regarding external connectivity (7 threats)
    {
        "r155_threat_id": "16.1",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["Cellular", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "16.2",
        "affected_components": ["Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Cellular"]
    },
    {
        "r155_threat_id": "16.3",
        "affected_components": ["Telematics Control Unit (TCU)", "Infotainment Unit (IVI)"],
        "affected_interfaces": ["Wi-Fi", "Bluetooth"]
    },
    {
        "r155_threat_id": "17.1",
        "affected_components": ["Infotainment Unit (IVI)"],
        "affected_interfaces": ["Wi-Fi", "USB"]
    },
    {
        "r155_threat_id": "18.1",
        "affected_components": ["Infotainment Unit (IVI)"],
        "affected_interfaces": ["USB"]
    },
    {
        "r155_threat_id": "18.2",
        "affected_components": ["Infotainment Unit (IVI)"],
        "affected_interfaces": ["USB"]
    },
    {
        "r155_threat_id": "18.3",
        "affected_components": ["OBD-II Diagnostic Port", "Central Gateway (CGW)"],
        "affected_interfaces": ["UDS over CAN"]
    },
    # 4.3.6 Potential targets or motivations for attack (8 threats)
    {
        "r155_threat_id": "19.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "19.3",
        "affected_components": ["Central Gateway (CGW)", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Automotive Ethernet", "CAN"]
    },
    {
        "r155_threat_id": "20.1",
        "affected_components": ["Powertrain ECU", "Central Gateway (CGW)"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "20.3",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["CAN", "Cellular"]
    },
    {
        "r155_threat_id": "20.5",
        "affected_components": ["Central Gateway (CGW)", "OBD-II Diagnostic Port"],
        "affected_interfaces": ["UDS over CAN", "CAN"]
    },
    {
        "r155_threat_id": "21.1",
        "affected_components": ["Central Gateway (CGW)", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Automotive Ethernet", "CAN"]
    },
    {
        "r155_threat_id": "22.2",
        "affected_components": ["Infotainment Unit (IVI)", "Telematics Control Unit (TCU)"],
        "affected_interfaces": ["Automotive Ethernet", "USB", "Cellular"]
    },
    {
        "r155_threat_id": "24.1",
        "affected_components": ["Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    # 4.3.7 Potential vulnerabilities if not sufficiently protected (6 threats)
    {
        "r155_threat_id": "26.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN"]
    },
    {
        "r155_threat_id": "26.2",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)"],
        "affected_interfaces": ["Automotive Ethernet", "Cellular"]
    },
    {
        "r155_threat_id": "27.1",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    },
    {
        "r155_threat_id": "28.1",
        "affected_components": ["Telematics Control Unit (TCU)", "Central Gateway (CGW)", "Infotainment Unit (IVI)"],
        "affected_interfaces": ["Automotive Ethernet", "CAN", "Cellular"]
    },
    {
        "r155_threat_id": "28.2",
        "affected_components": ["Central Gateway (CGW)", "OBD-II Diagnostic Port"],
        "affected_interfaces": ["UDS over CAN", "CAN"]
    },
    {
        "r155_threat_id": "29.2",
        "affected_components": ["Central Gateway (CGW)", "Powertrain ECU", "Brake ECU"],
        "affected_interfaces": ["CAN", "Automotive Ethernet"]
    }
]

def validate_selection():
    with open(THREATS_CSV, mode="r", encoding="utf-8") as f:
        threats_dict = {row["threat_id"]: row for row in csv.DictReader(f)}
        
    with open(VEHICLE_JSON, mode="r", encoding="utf-8") as f:
        v_data = json.load(f)
        valid_components = {c["name"] for c in v_data["components"]}
        valid_interfaces = {i["name"] for i in v_data["interfaces"]}
        
    print(f"Total proposed threats: {len(SELECTION)}")
    assert 40 <= len(SELECTION) <= 60, "Selection must be between 40 and 60 entries!"
    
    category_counts = {}
    for item in SELECTION:
        tid = item["r155_threat_id"]
        assert tid in threats_dict, f"Threat {tid} not found in r155_threats.csv!"
        row = threats_dict[tid]
        cat = row["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
        
        for c in item["affected_components"]:
            assert c in valid_components, f"Component {c} not in sample_vehicle.json!"
        for i in item["affected_interfaces"]:
            assert i in valid_interfaces, f"Interface {i} not in sample_vehicle.json!"
            
    print("\nVerified Category Distribution:")
    for cat, count in category_counts.items():
        print(f"  {cat}: {count} threats")
    assert len(category_counts) == 7, "All 7 categories must have entries!"
    print("\nAll 50 proposed threats strictly validated against active source CSV and vehicle architecture.")

if __name__ == "__main__":
    validate_selection()
