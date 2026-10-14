import os
import sys
import json
import http.server
import socketserver
import webbrowser
from urllib.parse import urlparse

PORT = 8081
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WEB_DIR = os.path.join(BASE_DIR, "web")

THREATS_JSON = os.path.join(BASE_DIR, "data", "library", "threat_library.json")
VEHICLE_JSON = os.path.join(BASE_DIR, "data", "system", "sample_vehicle.json")
CONFIG_JSON = os.path.join(BASE_DIR, "configs", "model_prompts_config.json")

class TARADashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        
        # API endpoints
        if parsed.path == "/api/threats":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(THREATS_JSON, "rb") as f:
                self.wfile.write(f.read())
            return
            
        elif parsed.path == "/api/vehicle":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(VEHICLE_JSON, "rb") as f:
                self.wfile.write(f.read())
            return

        elif parsed.path == "/api/config":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with open(CONFIG_JSON, "rb") as f:
                self.wfile.write(f.read())
            return

        return super().do_GET()

def run_server():
    os.chdir(WEB_DIR)
    handler = TARADashboardHandler
    # Allow address reuse to avoid port locking
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"\n==================================================================")
        print(f"  AUTOMOTIVE CYBERSECURITY TARA ASSISTANT - WEB DASHBOARD")
        print(f"==================================================================")
        print(f"  Status: Active & Serving Local Dashboard")
        print(f"  URL:    http://127.0.0.1:{PORT}")
        print(f"  Press Ctrl+C in terminal to stop the server.")
        print(f"==================================================================\n")
        try:
            webbrowser.open(f"http://127.0.0.1:{PORT}")
        except Exception:
            pass
        print(f"\n==================================================================")
        print(f"  AUTOMOTIVE CYBERSECURITY TARA ASSISTANT - WEB DASHBOARD")
        print(f"==================================================================")
        print(f"  Status: Active & Serving Local Dashboard")
        print(f"  URL:    http://127.0.0.1:{PORT}")
        print(f"  Press Ctrl+C in terminal to stop the server.")
        print(f"==================================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down dashboard server...")
            httpd.server_close()

if __name__ == "__main__":
    run_server()
