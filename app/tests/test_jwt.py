import requests

base_url = "http://localhost:8000"

# Register
res = requests.post(f"{base_url}/register", data={"username": "test", "password": "test"})
print("Register:", res.status_code, res.json())

# # Login
res = requests.post(f"{base_url}/token", data={"username": "test", "password": "test"})
token = res.json().get("access_token")
print("Token:", token)
#
# SMA
headers = {"Authorization": f"Bearer {token}"}
params = {
    "stock_symbol": "RAMASTEEL",
    "start_date": "2022-07-22",
    "end_date": "2022-12-31",
    "period": 20
}
print(headers)
res = requests.get(f"{base_url}/api/v1/indicators/sma", headers=headers, params=params)
print("SMA response:", res.status_code)
print(res.json())
