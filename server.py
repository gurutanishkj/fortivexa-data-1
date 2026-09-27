import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import http.server
import socketserver
import os
import sys
import json
import urllib.parse

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class FortivexaHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Prevent caching for live development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # Route / to index.html
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FortivexaHandler) as httpd:
        print(f"==================================================================")
        print(f"🛡️  FORTIVEXA CYBERCRIME INTELLIGENCE COMMAND CENTER SERVER")
        print(f"==================================================================")
        print(f"🌐 Website URL:  http://localhost:{PORT}")
        print(f"📂 Serving from: {DIRECTORY}")
        print(f"📊 Dataset:      10,000 merged NCRP cyber fraud records")
        print(f"🛑 Press Ctrl+C to stop the server")
        print(f"==================================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down FORTIVEXA Web Server...")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()
