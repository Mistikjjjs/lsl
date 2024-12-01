import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Configura tu token de Telegram aquí
TELEGRAM_TOKEN = "7878507254:AAGZ4i6ZPAnQKqBH4qAO2n-XCMU6Dl5E-Us"

# Función para descargar el enlace del video TikTok desde tmate.cc
def get_tiktok_download_link(video_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar sin interfaz gráfica
    driver = webdriver.Chrome(options=options)

    try:
        # Acceder a la página tmate.cc
        driver.get("https://tmate.cc/")
        time.sleep(2)

        # Buscar el campo de texto y enviar el enlace de TikTok
        input_box = driver.find_element(By.NAME, "url")
        input_box.send_keys(video_url)
        time.sleep(1)

        # Hacer clic en el botón de descarga
        download_button = driver.find_element(By.CLASS_NAME, "btn")
        download_button.click()
        time.sleep(5)

        # Obtener el enlace de descarga
        download_link = driver.find_element(By.XPATH, "//a[contains(@href, 'tiktokcdn')]").get_attribute("href")
        return download_link
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        driver.quit()

# Descargar el video desde el enlace obtenido
def download_video(download_link, output_path="downloaded_tiktok.mp4"):
    import requests
    response = requests.get(download_link, stream=True)
    if response.status_code == 200:
        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        return output_path
    else:
        print("Error al descargar el video")
        return None

# Comando /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("¡Hola! Envíame un enlace de TikTok con el comando /download para descargar el video.")

# Comando /download
def download(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("Por favor, envíame un enlace de TikTok con el comando /download <URL>.")
        return

    video_url = context.args[0]
    update.message.reply_text("Procesando tu solicitud, por favor espera...")

    # Obtener el enlace de descarga
    download_link = get_tiktok_download_link(video_url)
    if not download_link:
        update.message.reply_text("No se pudo obtener el enlace de descarga. Verifica el enlace de TikTok.")
        return

    # Descargar el video
    video_path = download_video(download_link)
    if not video_path:
        update.message.reply_text("Error al descargar el video.")
        return

    # Enviar el video al chat
    with open(video_path, "rb") as video:
        update.message.reply_video(video=video)

    # Eliminar el archivo temporal
    os.remove(video_path)

# Configuración principal del bot
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
