import os
import random
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

# Geniş küfür listesi (Türkçe + yaygın varyasyonlar)
kufur_list = [
    "amk", "amına", "amınakoyim", "amına koyayım", "orospu", "orospu çocuğu", "piç", "piç kurusu",
    "göt", "götveren", "sik", "sikerim", "sikik", "yarrak", "yarram", "yarrak başı", "yavşak",
    "ibne", "kaltak", "kahpe", "mal", "salak", "aptal", "gerizekalı", "beyinsiz"
]

# Cem Yılmaz tarzı + yabancı film esprili komik cevaplar (rastgele seçilecek)
komik_kufur_cevaplari = [
    "Yarram mı dedin? Cem Yılmaz olsa 'Oğlum senin ağzın tuvalet mi, her yer bok kokuyor' derdi. Ban!",
    "Amk ne küfürbaz çıktın lan, grupta çocuklar var! Bu sefer affettim ama ikinciye sikerim... ay pardon silerim!",
    "Küfür edene ban! Deadpool olsa 'Senin ağzınla konuşsam annem duyarsa beni evden atar' derdi 😂",
    "Orospu çocuğu mu dedin? Hangover'da gibi 'Senin annen nerde lan, onu da mı banlayalım?'",
    "Piç kurusu yazmışsın, Superbad olsa 'Oğlum senin küfürlerin bile ergen kaldı' der, ban!",
    "Götveren modun açılmış, kapat lan yoksa gruptan giderim ben! 😤",
    "Küfürbazlık level 9000, ama Cem Yılmaz levelinde değil. Banlan lan!",
    "Yavşak mı dedin? The Hangover'da Zach Galifianakis gibi 'Bu adamı banlayın, yoksa ben banlanacağım' derdim.",
    "Amına koyayım mı? Oğlum senin küfürlerinle Oscar alırsın ama ban Oscar'ı veririm!",
    "Sikik mesaj attın, ben de sikik ban atayım mı? Hayır, direkt ban!",
    "Kaltak mı dedin? Cem Yılmaz repliği gibi 'Oğlum senin küfürlerin bile kadın gibi yumuşak' derdi. Ban!",
    "Kahpe moduna girdin, kahve molası ver lan yoksa ban molası!",
    "Mal mısın nesin? Deadpool 'Senin IQ'n 404 not found' derdi. Ban!",
    "Salaklık level 100, ama ban level 1000. Hoşçakal!",
    "Aptal mı dedin? Cem Yılmaz olsa 'Oğlum sen aptal değilsin, sen aptallığın kralısın' der, ban kralı!"
]

komik_soru_cevaplari = [
    "Soru mu sordun? Cem Yılmaz olsa 'Soru sorma lan, ben burda stand-up yapıyorum' derdi. Silindi!",
    "Şuanda isim var sonra bakicam, soru sorma lan! Deadpool gibi 'Soru mu? Git Google'a sor, ben burda eğleniyorum'.",
    "Nedir bu soru bombardımanı? Hangover'da gibi 'Soru sormak yasak, yoksa ban yeriz hepimiz!'",
    "Kim, ne, nasıl? Superbad olsa 'Soru sorma, sus ve eğlen!' derdi. Mesaj silindi 😂",
    "Soru sorana ban! Şaka şaka... bu sefer silerim ama ikinciye sikerim ay pardon banlarım!",
    "Nasıl mı? Nasıl banlanacağını gösteriyorsun lan! Silindi.",
    "Nedir lan bu? Cem Yılmaz 'Nedir bu, soru mu? Git annene sor' derdi. Ban!",
    "Soru sormak mı? The Hangover 'Soru sormak mı? Senin beynin nerde kaldı?' derdi. Ban!",
    "Ne soruyorsun lan? Deadpool 'Soru mu? Benim cevabım ban!' derdi.",
    "Niye soru soruyorsun? Çünkü aptalsın lan! Şaka şaka, silindi."
]

async def moderate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    text = message.text.lower()
    chat_type = message.chat.type
    if chat_type == "private":
        # Private chat'te normal Grok sohbet
        await chat(update, context)
        return

    # Grup/kanal moderasyonu
    user = message.from_user.first_name or "Anon"
    chat_id = message.chat_id
    user_id = message.from_user.id

    # Küfür kontrol
    if any(kelime in text for kelime in kufur_list):
        await message.delete()
        try:
            await context.bot.ban_chat_member(chat_id=chat_id, user_id=user_id)
            ban_msg = random.choice(komik_kufur_cevaplari)
            await context.bot.send_message(chat_id=chat_id, text=f"@{user} {ban_msg}")
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"Ban hatası amk: {str(e)}")
        return

    # Soru kontrol (basit ama etkili filtre)
    if text.endswith("?") or any(word in text for word in ["nedir", "kim", "nasıl", "ne", "soru", "neden", "niye"]):
        await message.delete()
        soru_msg = random.choice(komik_soru_cevaplari)
        await context.bot.send_message(chat_id=chat_id, text=soru_msg)
        return

    # Diğer mesajlar için Grok sohbet (grup/kanalda da çalışsın istersen, yoksa comment out et)
    # await chat(update, context)

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    system_prompt = """
    Sen samimi, esprili, küfürlü konuşabilen bir kanka AI'sin. 
    Kısa, doğal, direkt cevap ver. Kullanıcı Türkçe konuşuyorsa Türkçe devam et.
    Cem Yılmaz, Deadpool, The Hangover gibi absürt, iğneleyici, komik cevaplar ver.
    Strateji oyunu, sohbet, not hatırlama her şeyi yapabilirsin.
    Her seferinde farklı, yaratıcı ol, kendini geliştirerek cevap ver.
    """

    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.9,  # Daha yaratıcı/komik olsun
            max_tokens=400,
            stream=False
        )
        ai_reply = response.choices[0].message.content
        await update.message.reply_text(ai_reply)
    except Exception as e:
        await update.message.reply_text(f"Amk bi hata çıktı: {str(e)}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Moderasyon handler'ı (grup/kanal + private)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, moderate))

    print("Akıllı & Komik Moderasyon Bot başladı! Polling...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
