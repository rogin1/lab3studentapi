"""
Quick API test — runs against the live runserver.
Demonstrates:  Unauthorized (401) → Get Token → Authorized (200)
"""
import urllib.request
import urllib.error
import json

BASE = "http://127.0.0.1:8000"

def request(url, data=None, headers={}):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

print("=" * 55)
print("  STUDENT API — JWT Authentication Test")
print("=" * 55)

# 1. Unauthorized request
print("\n[1] Unauthorized GET /api/students/  (no token)")
status, data = request(f"{BASE}/api/students/")
print(f"    Status : {status}")
print(f"    Body   : {data}")

# 2. Get JWT token
print("\n[2] POST /api/token/  (get access token)")
status, data = request(
    f"{BASE}/api/token/",
    data={"username": "rogin", "password": "rogin123"},
    headers={"Content-Type": "application/json"},
)
print(f"    Status : {status}")
if status == 200:
    token = data["access"]
    print(f"    Access : {token[:40]}...")
    print(f"    Refresh: {data['refresh'][:40]}...")
else:
    print(f"    Error  : {data}")
    exit()

# 3. Authorized request
print("\n[3] Authorized GET /api/students/  (with Bearer token)")
status, data = request(
    f"{BASE}/api/students/",
    headers={"Authorization": f"Bearer {token}"},
)
print(f"    Status : {status}")
print(f"    Body   : {json.dumps(data, indent=2)}")

print("\n" + "=" * 55)
print("  ✅ All checks passed!" if status == 200 else "  ❌ Something went wrong.")
print("=" * 55)
