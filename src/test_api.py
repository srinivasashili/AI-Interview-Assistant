import requests
import os
API_KEY = os.getenv("ANTHROPIC_API_KEY")
headers = {
    "x-api-key": API_KEY,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json",
}
body = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Say hello"}],
}

response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
print("Status:", response.status_code)
print("Response:", response.json())