import os
import time
import gspread
from telegram import Bot
from oauth2client.service_account import ServiceAccountCredentials

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
SHEET_TAB = os.getenv("GOOGLE_SHEET_TAB_NAME")
INTERVAL = int(os.getenv("CHECK_INTERVAL_SECONDS", "300"))

bot = Bot(token=TELEGRAM_TOKEN)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_TAB)

seen = set()

def check_updates():
    global seen
    rows = sheet.get_all_records()
    for row in rows:
        key = tuple(row.items())
        if key not in seen:
            seen.add(key)
            message = "\n".join([f"{k}: {v}" for k, v in row.items()])
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"📩 New Partner Request:\n{message}")

if __name__ == "__main__":
    while True:
        check_updates()
        time.sleep(INTERVAL)