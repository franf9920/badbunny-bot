import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://www.allaccess.com.ar/event/badbunny'
CHECK_INTERVAL = 60  # segundos

bot = Bot(token=TELEGRAM_TOKEN)

def check_tickets():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        buy_button = soup.find('a', class_='button-buy')
        if buy_button and "entradas" in buy_button.text.lower():
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al revisar la página: {e}")
        return False

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Error enviando mensaje de Telegram: {e}")

def main():
    while True:
        print("Revisando disponibilidad...")
        if check_tickets():
            send_telegram_message("¡HAY ENTRADAS PARA BAD BUNNY!")
            break
        else:
            print("No hay entradas disponibles aún.")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
