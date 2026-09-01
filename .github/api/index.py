import os
import sys

# Add root directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html_content = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>BLJ Classes Portal</title>
            </head>
            <body style="font-family: Arial, sans-serif; text-align: center; margin-top: 80px; background-color: #0f172a; color: #f8fafc;">
                <h2>BLJ Classes Portal</h2>
                <p>Serverless environment initialized on Vercel.</p>
                <p style="color: #94a3b8; font-size: 14px;">Note: Streamlit apps require a persistent websocket server process.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return

    def do_POST(self):
        self.do_GET()
