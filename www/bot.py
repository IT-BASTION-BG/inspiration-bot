from datetime import datetime
import os, random, time, requests
from dotenv import load_dotenv
from quotes import INSIGHTFUL_QUOTES

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Глобална променлива за памет на последния цитат
last_quote = None


def get_random_quote() -> str:
  global last_quote
  if len(INSIGHTFUL_QUOTES) <= 1:
    return random.choice(INSIGHTFUL_QUOTES)

  # Теглим нов цитат, докато е различен от последния изпратен
  quote = random.choice(INSIGHTFUL_QUOTES)
  while quote == last_quote:
    quote = random.choice(INSIGHTFUL_QUOTES)

  last_quote = quote
  return quote


def push_to_discord(message: str):
  payload = {"content": message}
  response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

  if response.status_code == 204:
    print(
        f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Успешно пратено"
        " съобщение в Discord"
    )
  else:
    print(
        f"Грешка при пращане: {response.status_code} - {response.text}"
    )


if __name__ == "__main__":
  if not DISCORD_WEBHOOK_URL:
    print("Грешка: DISCORD_WEBHOOK_URL не е намерен в .env файла!")
    exit(1)

  print(
      "Inspiration ботът стартира (режим: сутрин в 08:00 и вечер в 20:00)..."
  )

  # Пазим дата и част от деня ("morning" или "evening"), за да не прати два пъти в рамките на същия слот
  last_sent_slot = None

  while True:
    try:
      now = datetime.now()
      current_hour = now.hour
      current_date = now.date()

      # Определяме в кой времеви прозорец се намираме
      target_slot = None
      message_prefix = ""

      if current_hour == 8:
        target_slot = f"{current_date}_morning"
        message_prefix = "Добро утро! ☕\n"
      elif current_hour == 20:
        target_slot = f"{current_date}_evening"
        message_prefix = "Добър вечер! ☕\n"

      # Ако е 08:00 или 20:00 и още не сме пращали за този слот днес
      if target_slot and last_sent_slot != target_slot:
        quote = get_random_quote()
        full_message = f"{message_prefix}💡 {quote}"

        push_to_discord(full_message)
        last_sent_slot = target_slot

        # Заспиваме за малко повече от час, за да не зацепи в същия час отново
        time.sleep(4000)
      else:
        # Проверява на всеки 30 минути (1800 секунди) за следващия час
        time.sleep(1800)

    except Exception as e:
      print(f"Възникна грешка: {e}")
      time.sleep(60)