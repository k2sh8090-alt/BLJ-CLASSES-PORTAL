import os
import sys

# Ensure the root directory is in the path so it can find app.py or dependencies
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # A simple response or redirect notice since Streamlit requires WebSockets 
        # which standard Vercel serverless functions cannot stream persistently.
        html_content = """
        <html>
            <head><title>BLJ Classes Portal</title></head>
            <body style="font-family: sans-serif; text-align: center; margin-top: 50px;">
                <h2>BLJ Classes Portal - Serverless Endpoint</h2>
                <p>Vercel serverless functions are active. Note that Streamlit natively requires a persistent WebSocket server.</p>
            </body>
        </html>
        """
        self.wfile.write(html_content.encode('utf-8'))
        return
