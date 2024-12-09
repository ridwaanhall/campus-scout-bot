import os
import requests
from dotenv import load_dotenv

def main():
    load_dotenv()

    TELE_BOT_TOKEN = os.getenv('TELE_BOT_TOKEN')

    if not TELE_BOT_TOKEN:
        raise ValueError("TELE_BOT_TOKEN is not set in the environment variables")

    webhook_url = 'https://campus-scout-bot.vercel.app'
    telegram_api_url = f'https://api.telegram.org/bot{TELE_BOT_TOKEN}/setWebhook'

    data = {
        'url': webhook_url
    }

    try:
        response = requests.post(telegram_api_url, data=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error setting webhook: {e}")

if __name__ == "__main__":
    main()