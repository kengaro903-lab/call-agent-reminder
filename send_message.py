import os
import sys
import json
import requests
from datetime import datetime, timedelta
import pytz

# --------------------------------------------
# Load environment variables from GitHub Secrets
# --------------------------------------------
WHAPI_TOKEN = os.getenv("WHAPI_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")
MENTION_WAID = os.getenv("MENTION_WAID")
DISPLAY_NAME = os.getenv("DISPLAY_NAME")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
IST_DAY = os.getenv("IST_DAY", "03")
IST_TIME = os.getenv("IST_TIME", "13:50")

API_BASE = "https://gate.whapi.cloud"

# --------------------------------------------
# Helper function for logging and failing cleanly
# --------------------------------------------
def fail(msg):
    print(f"[error] {msg}")
    sys.exit(1)

# --------------------------------------------
# Check if required env vars exist
# --------------------------------------------
missing = [v for v in ["WHAPI_TOKEN", "GROUP_ID", "MENTION_WAID", "DISPLAY_NAME"] if not globals()[v]]
if missing:
    fail(f"Missing env vars: {', '.join(missing)}")

# --------------------------------------------
# (Optional) Time gate – disabled for testing
# --------------------------------------------
def ist_gate():
    # Temporarily disabled to allow testing anytime
    # Uncomment later for strict scheduling
    pass

# --------------------------------------------
# Send the message through Whapi API
# --------------------------------------------
def send_text():
    """Send the WhatsApp message with one mention."""
    url = f"{API_BASE}/messages/text"
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }

    # ✅ Proper message body with mention text
    body_text = f"please confirm if rent for Raintree flat has been received this month? @{DISPLAY_NAME}"

    payload = {
        "to": GROUP_ID,
        "body": body_text,
        "mentions": [MENTION_WAID]
    }

    print(f"[send] Sending to {GROUP_ID}...")
    print(f"[debug] Payload: {json.dumps(payload)}")

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"[http] {r.status_code} {r.text}")
    except requests.exceptions.RequestException as e:
        fail(f"Request failed: {e}")

    if r.status_code != 200:
        fail(f"Whapi API rejected the request: {r.text}")

    try:
        resp = r.json()
    except Exception:
        fail("Invalid or non-JSON response from Whapi.")

    message_id = (((resp or {}).get("message")) or {}).get("id")
    if message_id:
        print(f"[status] Message sent successfully with ID: {message_id}")
    else:
        print(f"[warn] No message ID returned from API. Full response: {resp}")
    return message_id


# --------------------------------------------
# Main execution
# --------------------------------------------
if __name__ == "__main__":
    print(f"[start] WhatsApp Rent Reminder – {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ist_gate()  # time window disabled for now
    message_id = send_text()
    if not message_id:
        fail("Message send failed – no ID received.")
    print("[done] Message delivered successfully ✅")
