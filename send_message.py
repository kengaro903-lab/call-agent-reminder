import os
import requests
import pytz
from datetime import datetime

# Load secrets
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
MENTION_WAID = os.getenv("MENTION_WAID")

if not WHAPI_TOKEN or not GROUP_ID:
    print("❌ Missing required environment variables.")
    exit(1)

# Current IST time
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
formatted_time = now.strftime("%I:%M %p")

# Message text
message = f"Please confirm if rent for Raintree flat has been received this month? @{MENTION_WAID or 'user'}"

# Prepare request
url = "https://gate.whapi.cloud/messages/text"
headers = {"Authorization": f"Bearer {WHAPI_TOKEN}", "Content-Type": "application/json"}
payload = {"to": GROUP_ID, "body": message}

# Send message
print("📨 Sending WhatsApp message...")
response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("✅ Message sent successfully!")
else:
    print("❌ Failed to send message. Check your WHAPI token or group ID.")
