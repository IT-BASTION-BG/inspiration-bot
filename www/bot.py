from datetime import datetime
import random, time, requests, os
from dotenv import load_dotenv
from quotes import INSIGHTFUL_QUOTES

load_dotenv()  # Load environment variables from .env file

# Webhook URL-а, който вземаш от настройките на Discord канала -> Integrations -> Webhooks
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def push_quote(quote: str):
  payload = {"content": f"💡 {quote}"}
  response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

  if response.status_code == 204:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Успешно пратен inspiration")
  else:
    print(f"Грешка при пращане: {response.status_code}")


if __name__ == "__main__":
  if not DISCORD_WEBHOOK_URL:
    print("Грешка: DISCORD_WEBHOOK_URL не е намерен в .env файла!")
    exit(1)

  print("Inspiration ботът стартира (с активен нощен режим 20:00 - 08:00)...")

  while True:
    try:
      current_hour = datetime.now().hour

      # Нощен режим: ако часът е между 20:00 (вкл.) и 08:00 (изкл.)
      if current_hour >= 20 or current_hour < 8:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] Нощ е (час:"
            f" {current_hour}). Ботът спи..."
        )
        # Проверява по-рядко през нощта (например на всеки час - 3600 сек)
        time.sleep(3600)
        continue

      # Дневен режим: праща цитат
      quote = random.choice(INSIGHTFUL_QUOTES)
      push_quote(quote)

    except Exception as e:
      print(f"Възникна грешка: {e}")

    # Проверява на всеки 30 минути (1800 секунди) през деня
    time.sleep(1800)