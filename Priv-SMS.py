from telegram import Update
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = '7646020619:AAEYQE2EskDUPNfHUsgi_1-3mbnJnlwUoXY'

AUTHORIZED_USERS = [8039965168]  # Kendi Telegram user ID'ni buraya yaz

def safe_decode(output_bytes):
    try:
        return output_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return output_bytes.decode('latin1', errors='replace')

async def run_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in AUTHORIZED_USERS:
        await update.message.reply_text("Erişim reddedildi.")
        return

    cmd = update.message.text
    try:
        output_bytes = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=10)
        output = safe_decode(output_bytes)
    except subprocess.CalledProcessError as e:
        output = safe_decode(e.output)
    except subprocess.TimeoutExpired:
        output = "Komut zaman aşımına uğradı."

    if not output:
        output = "Çıktı yok."
    await update.message.reply_text(f"📤 Çıktı:\n{output}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, run_command))
    print("🤖 Bot çalışıyor...")
    app.run_polling()
