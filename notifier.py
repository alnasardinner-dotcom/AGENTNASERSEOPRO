import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    def __init__(self, bot_token: str = "", chat_id: str = ""):
        self.bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")

    def send_message(self, message: str):
        """Send instant real-time alert message to Telegram."""
        if not self.bot_token or not self.chat_id:
            print("[TelegramNotifier] Telegram Bot Token or Chat ID not set. Skipping push notification.")
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload, timeout=8)
            if res.status_code == 200:
                print("[TelegramNotifier] Real-time alert sent to Telegram successfully!")
                return True
        except Exception as e:
            print(f"[TelegramNotifier] Error sending Telegram alert: {e}")
        return False
