import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# Variables de entorno
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# URL del evento
URL = 'https://www.allaccess.com.ar/event/linkin-park-venta-general'
CHECK_INTERVAL = 30  # segundos

# Inicializar el bot de Telegram
bot = Bot(token=TELEGRAM_TOKEN)

def start_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # correr sin abrir ventana
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    return driver

def check_tickets(driver):
    try:
        driver.get(URL)
        time.sleep(5)  # esperar a que cargue el JavaScript
        
        # Buscar el botón que diga "entradas"
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if "entradas" in button.text.lower():
                return True
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if "entradas" in link.text.lower():
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
    driver = start_browser()
    while True:
        print("🔎 Revisando disponibilidad...", flush=True)
        if check_tickets(driver):
            print("🎟️ Entradas disponibles detectadas, enviando mensaje a Telegram...", flush=True)
            send_telegram_message("¡HAY ENTRADAS PARA BAD BUNNY! 🎟️🔥")
            break
        else:
            print("❌ No hay entradas disponibles aún.", flush=True)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
