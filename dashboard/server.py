"""
Dashboard HTTP Server
Serves the intelligentOne monitoring dashboard and API endpoints
"""

import http.server
import socketserver
import json
import os
from pathlib import Path

# Import Blueprint Vault
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from blueprint_vault import BlueprintVault

PORT = int(os.getenv('PORT', 8080))
BLUEPRINT_PATH = os.getenv('BLUEPRINT_STORAGE_PATH', '../blueprints')

# Initialize Blueprint Vault
vault = BlueprintVault(storage_path=BLUEPRINT_PATH)


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for dashboard API and static files."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/api/blueprints':
            self.serve_blueprints_api()
        elif self.path == '/':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def serve_blueprints_api(self):
        """Serve blueprint data as JSON API."""
        try:
            # Load all blueprints
            blueprints = vault.load_all_blueprints()
            stats = vault.get_stats()
            
            # Prepare response
            response = {
                'blueprints': blueprints,
                'stats': stats,
                'status': 'success'
            }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # CORS for local dev
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
        
        except Exception as e:
            # Error response
            error_response = {
                'error': str(e),
                'status': 'error'
            }
            
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(error_response).encode())
    
    def log_message(self, format, *args):
        """Custom logging format."""
        print(f"📊 Dashboard: {args[0]}")


def run_server():
    """Start the dashboard server."""
    # Change to dashboard directory
    dashboard_dir = Path(__file__).parent
    os.chdir(dashboard_dir)
    
    print("🎨 Dashboard server starting...")
    print(f"📊 Serving on http://localhost:{PORT}")
    print(f"💾 Blueprint Vault: {BLUEPRINT_PATH}")
    print(f"🔄 Auto-refresh: 30 seconds")
    print("\nPress Ctrl+C to stop")
    print("=" * 50)
    
    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 Dashboard server stopped")
            pass


if __name__ == "__main__":
    run_server()
