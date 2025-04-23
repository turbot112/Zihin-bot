import os
import telegram

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = -1004634117873  # Grup chat ID

print(f"[DEBUG] TOKEN: {BOT_TOKEN}")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN ortam değişkeni eksik!")

try:
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text="Test sinyali: Her şey yolunda aşkım!")
    print("Mesaj başarıyla gönderildi.")
except telegram.error.Unauthorized:
    raise Exception("TOKEN geçersiz! Lütfen yeni token alıp Render'a gir.")
