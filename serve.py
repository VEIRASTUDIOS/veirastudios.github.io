import http.server
import socketserver
import os
import sys

BASE_PORT = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 3000))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

import json

class NoCacheHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/api/submit-inquiry':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                print("\n" + "="*60)
                print("📨 [LOCAL BACKEND] NEW PROJECT INQUIRY RECEIVED FOR veira.studio7@gmail.com:")
                for k, v in data.items():
                    print(f"  {k}: {v}")
                print("="*60 + "\n")
                
                # Save to inquiries.json
                inquiries_file = os.path.join(DIRECTORY, "inquiries.json")
                inquiries = []
                if os.path.exists(inquiries_file):
                    try:
                        with open(inquiries_file, "r", encoding="utf-8") as f:
                            inquiries = json.load(f)
                    except Exception:
                        inquiries = []
                inquiries.append(data)
                with open(inquiries_file, "w", encoding="utf-8") as f:
                    json.dump(inquiries, f, indent=2)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Inquiry recorded"}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
                return
        super().do_POST()

socketserver.TCPServer.allow_reuse_address = True

port = BASE_PORT
httpd = None
while port < BASE_PORT + 50:
    try:
        httpd = socketserver.TCPServer(("", port), NoCacheHTTPRequestHandler)
        break
    except OSError:
        port += 1

if not httpd:
    print(f"Error: Could not find an available port starting from {BASE_PORT}.")
    sys.exit(1)

with httpd:
    print(f"Serving at http://localhost:{port} (directory: {DIRECTORY}) with NO-CACHE")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
