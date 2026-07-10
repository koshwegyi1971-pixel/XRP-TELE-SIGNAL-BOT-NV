import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from app.config import PORT

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"XRP Signal Bot NV - Healthy")

    def log_message(self, format, *args):
        return

def start_health_server():
    server = HTTPServer(('0.0.0.0', PORT), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    print(f"Health server started on port {PORT}")
