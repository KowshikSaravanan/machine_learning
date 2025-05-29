import requests
import json
import sys

# Import the token generator directly from your app
try:
    from app.jwt import create_token
except ModuleNotFoundError:
    print("ERROR: Make sure you run this script from your project root where 'app/' exists.")
    sys.exit(1)

# === Configuration ===
API_URL = "http://localhost:8000/predict"
USER_ID = "alice"  # Or any username you like
FEATURES = [650, 0, 1, 42, 4, 102000.50, 2, 1, 1, 80000.00]  # Example customer

# === Generate JWT Token ===
token = create_token(USER_ID)
if isinstance(token, bytes):
    token = token.decode()  # pydantic/jwt versions may return bytes or str

print("JWT Token:", token)

# === Prepare Headers and Payload ===
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "features": FEATURES
}

# === Make API Request ===
print(f"Making request to {API_URL}...")
response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

print(f"Status Code: {response.status_code}")
try:
    print("Response:", response.json())
except Exception:
    print("Raw Response:", response.text)
