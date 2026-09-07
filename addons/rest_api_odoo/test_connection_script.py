import urllib.request
import json

url = "http://localhost:8088/odoo_connect"
data = {
    "db": "test_db",
    "login": "admin",
    "password": "admin"
}
json_data = json.dumps(data).encode('utf-8')

req = urllib.request.Request(url, data=json_data, method='POST')
req.add_header('Content-Type', 'application/json')

print(f"Testing POST to {url}...")
try:
    with urllib.request.urlopen(req) as response:
        print(f"Status Code: {response.status}")
        print(f"Response Body: {response.read().decode('utf-8')[:500]}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} {e.reason}")
    print(f"Response: {e.read().decode('utf-8')[:500]}")
except Exception as e:
    print(f"Script Error: {e}")
