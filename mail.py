import os
import telegram

# Bot token'ı environment'dan alınıyor
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Güncel, doğru grup chat ID
CHAT_ID = -1002512446830  # Kazananlar grubun ID’si

# Debug log (Render loglarında görünür)
print(f"[DEBUG] TOKEN: {BOT_TOKEN}")

# Hata varsa yakala
if not BOT_TOKEN:
    raise Exception("BOT_TOKEN ortam değişkeni eksik!")

try:
    # Botu başlat
    bot = telegram.Bot(token=BOT_TOKEN)
    
    # Test mesajı gönder
    bot.send_message(chat_id=CHAT_ID, text="Test sinyali: Her şey yolunda aşkım!")
    print("Mesaj başarıyla gönderildi.")
except telegram.error.Unauthorized:
    raise Exception("TOKEN geçersiz! Lütfen yeni token alıp Render'a gir.")
except telegram.error.BadRequest as e:
    raise Exception(f"BadRequest hatası: {e}")
except Exception as e:
    raise Exception(f"Genel hata: {e}")
