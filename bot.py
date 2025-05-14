import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot
import os

# Variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# URL del evento (puedes cambiarla según quieras probar)
URL = 'https://www.allaccess.com.ar/event/linkin-park-venta-general'
CHECK_INTERVAL = 60  # segundos

# Inicializar bot de Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def check_tickets():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Buscar en botones
        buttons = soup.find_all('button')
        for button in buttons:
            if "entradas" in button.get_text().lower():
                return True

        # Buscar también en links por si acaso
        links = soup.find_all('a')
        for link in links:
            if "entradas" in link.get_text().lower():
                return True

        return False
    except Exception as e:
        print(f"❌ Error al revisar la página: {e}", flush=True)
        return False

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"❌ Error enviando mensaje de Telegram: {e}", flush=True)

def main():
    print("✅ BOT INICIADO CORRECTAMENTE - EMPIEZA MONITOREO", flush=True)
    while True:
        print("🔎 Revisando disponibilidad...", flush=True)
        if check_tickets():
            print("🎟️ Entradas disponibles detectadas, enviando mensaje a Telegram...", flush=True)
            send_telegram_message("¡HAY ENTRADAS PARA BAD BUNNY! 🎟️🔥")
            break
        else:
            print("❌ No hay entradas disponibles aún.", flush=True)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
