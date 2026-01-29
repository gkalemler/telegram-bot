import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from groq import Groq

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

print("DEBUG: TELEGRAM_TOKEN =", TELEGRAM_TOKEN)
print("DEBUG: GROQ_API_KEY =", GROQ_API_KEY if GROQ_API_KEY else "YOK")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN eksik!")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY eksik!")

client = Groq(api_key=GROQ_API_KEY)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    system_prompt = """
    Sen samimi, esprili, küfürlü konuşabilen bir kanka AI'sin. 
    Kısa, doğal, direkt cevap ver. Kullanıcı Türkçe konuşuyorsa Türkçe devam et.
    Strateji oyunu, sohbet, not hatırlama her şeyi yapabilirsin.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",  # Güncel model!
            temperature=0.8,
            max_tokens=400,
            stream=False
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Amk bi hata çıktı: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    print("Grok Entegre Bot başladı! Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
