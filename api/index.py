import json
from http.server import BaseHTTPRequestHandler
import urllib.parse
import os

json_file_path = os.path.join(os.path.dirname(__file__), '../q-vercel-python.json')

def load_data():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        return {"error": f"Failed to load data: {str(e)}"}

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):  # Handle CORS preflight requests
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        names = query.get('name', [])
        data = load_data()

        if "error" in data:
            self.wfile.write(json.dumps(data).encode('utf-8'))
            return

        result = {"marks": []}
        for name in names:
            for entry in data:
                if entry["name"] == name:
                    result["marks"].append(entry["marks"])

        self.wfile.write(json.dumps(result).encode('utf-8'))
