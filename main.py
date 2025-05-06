import requests
import time
import json

TELEGRAM_TOKEN = "7904643020:AAEqjQstRYjb0U-qOtj5OFBUP_srtGIZnf4"
CHAT_ID = "79857965"

TESLA_API_URL = "https://www.tesla.com/inventory/api/v1/inventory-results"

QUERY_PAYLOAD = {
    "query": {
        "model": "my",
        "condition": "new",
        "arrangeby": "plh",
        "zip": "34080",
        "range": 0,
        "market": "TR",
        "language": "tr",
        "super_region": "emea"
    },
    "offset": 0,
    "count": 50,
    "outsideSearch": False
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

previous_ids = set()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram error: {e}")

def check_tesla_inventory():
    global previous_ids
    try:
        response = requests.get(
            TESLA_API_URL,
            params={"query": json.dumps(QUERY_PAYLOAD)},
            headers=HEADERS,
            timeout=30
        )
        data = response.json()
        vehicles = data.get("results", [])

        new_ids = set(v["VIN"] for v in vehicles)
        added_ids = new_ids - previous_ids

        if added_ids:
            for v in vehicles:
                if v["VIN"] in added_ids:
                    msg = f"🚗 *Yeni Tesla Model Y!*\n\n"
                    msg += f"*Model:* {v.get('PAINT_NAME', 'Bilinmiyor')}\n"
                    msg += f"*Fiyat:* {v.get('PricingDetail', {}).get('totalPrice', 'Yok')} TL\n"
                    msg += f"[İncele]({v.get('VIN', '')})"
                    send_telegram_message(msg)

        previous_ids = new_ids

    except Exception as e:
        send_telegram_message(f"❌ Bot hata aldı: {e}")

while True:
    check_tesla_inventory()
    time.sleep(15)
