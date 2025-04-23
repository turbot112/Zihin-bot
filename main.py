import os
import telegram

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = -1004634117873  # Güncel grup ID

print(f"[DEBUG] TOKEN: {BOT_TOKEN}")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN ortam değişkeni tanımlı değil!")

try:
    bot = telegram.Bot(token=BOT_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text="Test sinyali: BTC/USDT 10x LONG - Giriş: 62000")
    print("Mesaj başarıyla gönderildi.")
except telegram.error.Unauthorized:
    raise Exception("TOKEN geçersiz! Lütfen yeni bir bot token gir.")
except Exception as e:
    print(f"HATA: {e}")
