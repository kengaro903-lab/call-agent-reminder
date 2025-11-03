import os
import requests
import pytz
from datetime import datetime

# Load environment variables
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
MENTION_WAID = os.getenv("MENTION_WAID")  # Example: 918483826996@c.us
MENTION_NAME = "Sanket"  # The visible name

if not WHAPI_TOKEN or not GROUP_ID or not MENTION_WAID:
    print("❌ Missing required environment variables.")
    exit(1)

# Current IST time
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)
formatted_time = now.strftime("%I:%M %p")

# WhatsApp message
message_text = f"Please confirm if rent for Raintree flat has been received this month? @{MENTION_NAME}"

# Whapi API setup
url = "https://gate.whapi.cloud/messages/text"
headers = {"Authorization": f"Bearer {WHAPI_TOKEN}", "Content-Type": "application/json"}
payload = {
    "to": GROUP_ID,
    "body": message_text,
    "mentions": [MENTION_WAID]  # FIXED: must be a list of strings
}

# Send message
print("📨 Sending WhatsApp message...")
response = requests.post(url, headers=headers, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.text)

if response.status_code == 200:
    print("✅ Message sent successfully!")
else:
    print("❌ Failed to send message. Check your WHAPI token or group ID.")
