import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Token'ı environment variable'dan oku (Render'da TELEGRAM_TOKEN olarak tanımladığın için)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Debug için token'ı loga yazdır (sorun olursa logda görürsün)
print("DEBUG: TELEGRAM_TOKEN =", TELEGRAM_TOKEN)

# Token yoksa hata ver ki hemen anlayalım
if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable bulunamadı! Render'da TELEGRAM_TOKEN ekle.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Bot çalışıyor. 😎")

async def mesaj(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Gelen mesajı echo yap (yani tekrar gönder)
    await update.message.reply_text(f"Echo: {update.message.text}")

def main():
    # Application'ı builder ile oluştur
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Komut handler'ları ekle
    app.add_handler(CommandHandler("start", start))

    # Herhangi bir metin mesajına cevap verecek handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj))

    # Polling ile başlat (webhook yerine basit polling kullanıyoruz)
    print("Bot polling ile başlatılıyor...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
