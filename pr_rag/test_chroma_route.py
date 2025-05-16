import requests

url = "https://notifications.codeominous.com/api/v1/heartbeat"

response = requests.get(url)

if response.status_code == 200:
    print("✅ Chroma route is healthy!")
    print("Response:", response.json())
else:
    print("❌ Chroma route failed:", response.status_code, response.text)
