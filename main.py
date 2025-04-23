import os
import telebot
import requests
from telebot import types
from datetime import datetime

# Ortam değişkeninden token al
BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Güncel grup chat ID (Kazananlar)
CHAT_ID = -1002512446830

# Admin ve destek ID'leri
admin_id = 1769686760
destek_id = 1121214662

# VIP kullanıcılar
vip_users = [admin_id, destek_id]

# Kullanıcı logları
user_logs = {}

# START komutu
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('/sinyal', '/vipsinyal')
    markup.row('/ozet', '/fiyat', '/id', '/odeme')
    markup.row('/destek', '/vip')
    if message.from_user.id == admin_id:
        markup.row('/vip_ekle', '/vip_sil')
    bot.send_message(message.chat.id, "Hoş geldin! Aşağıdaki komutlarla botu kullanabilirsin:", reply_markup=markup)

# ID komutu
@bot.message_handler(commands=['id'])
def send_id(message):
    bot.reply_to(message, f"Telegram ID’n: {message.from_user.id}")

# Ödeme bilgisi
@bot.message_handler(commands=['odeme'])
def send_payment_info(message):
    bot.send_message(message.chat.id,
        "VIP üyelik için ödeme bilgileri:\n"
        "Papara: 1492701376\n\n"
        "VIP Paketler:\n"
        "- 1 Ay: 300 TL\n"
        "- 3 Ay: 750 TL\n"
        "- 1 Yıl: 1200 TL\n"
        "- Ömür Boyu: 1500 TL\n\n"
        "Formu doldur: https://docs.google.com/forms/d/e/1FAIpQLScXsoYjvQWewMIJFOenljRpdl3LqwnbkGPNjmIrAWeL195fHA/viewform"
    )

# VIP bilgi
@bot.message_handler(commands=['vip'])
def send_vip_info(message):
    bot.reply_to(message,
        "VIP üyelik ile neler kazanırsın?\n"
        "- Özel sinyaller\n- Günlük kazanç özeti\n- Otomatik sistem erişimi\n"
        "- Sadece sana özel analizler\n\n"
        "VIP olmak için: /odeme yaz ve formu doldur."
    )

# Ücretsiz sinyal
@bot.message_handler(commands=['sinyal'])
def send_signal(message):
    log_user(message.from_user.id, "Ücretsiz sinyal aldı")
    bot.send_message(message.chat.id, "Ücretsiz Sinyal: BTC/USDT 10x Long\nGiriş: 62.000\nTP: 63.800\nSL: 61.000")

# VIP sinyal
@bot.message_handler(commands=['vipsinyal'])
def send_vip_signal(message):
    if message.from_user.id in vip_users:
        log_user(message.from_user.id, "VIP sinyal aldı")
        bot.send_message(message.chat.id, "VIP Sinyal: ETH/USDT 20x Long\nGiriş: 3.100\nTP: 3.250\nSL: 2.950")
    else:
        bot.reply_to(message, "Bu komut sadece VIP üyeler içindir. VIP olmak için: /odeme")

# Günlük özet
@bot.message_handler(commands=['ozet'])
def send_summary(message):
    if message.from_user.id in vip_users:
        log_user(message.from_user.id, "Günlük özet aldı")
        bot.send_message(message.chat.id,
            "Günlük Kazanç Özeti:\n- BTC: +6.2%\n- ETH: +3.1%\n- SOL: +8.9%"
        )
    else:
        bot.reply_to(message, "Bu komut sadece VIP üyeler içindir.")

# Coin fiyatı sorgulama
@bot.message_handler(commands=['fiyat'])
def coin_price_handler(message):
    try:
        msg_parts = message.text.split()
        if len(msg_parts) != 2:
            bot.reply_to(message, "Kullanım: /fiyat BTC")
            return
        coin = msg_parts[1].upper()
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin}USDT"
        response = requests.get(url)
        data = response.json()
        price = float(data['price'])
        bot.reply_to(message, f"{coin} şu anki fiyatı: {price:.2f} USDT")
    except Exception:
        bot.reply_to(message, "Coin fiyatı alınamadı veya coin geçersiz.")

# Destek komutu
@bot.message_handler(commands=['destek'])
def destek_handler(message):
    destek_mesaj = f"Kullanıcı destek istedi: {message.from_user.id} - {message.from_user.first_name}"
    bot.send_message(admin_id, destek_mesaj)
    bot.send_message(destek_id, destek_mesaj)
    bot.reply_to(message, "Destek talebin alındı. Ekibimiz seninle iletişime geçecek.")

# VIP ekle / sil (admin)
@bot.message_handler(commands=['vip_ekle'])
def add_vip(message):
    if message.from_user.id != admin_id:
        return
    try:
        new_id = int(message.text.split()[1])
        if new_id not in vip_users:
            vip_users.append(new_id)
            bot.reply_to(message, f"{new_id} artık VIP!")
        else:
            bot.reply_to(message, "Zaten VIP.")
    except:
        bot.reply_to(message, "Kullanım: /vip_ekle 123456789")

@bot.message_handler(commands=['vip_sil'])
def remove_vip(message):
    if message.from_user.id != admin_id:
        return
    try:
        del_id = int(message.text.split()[1])
        if del_id in vip_users:
            vip_users.remove(del_id)
            bot.reply_to(message, f"{del_id} VIP listesinden çıkarıldı.")
        else:
            bot.reply_to(message, "Bu ID VIP değil.")
    except:
        bot.reply_to(message, "Kullanım: /vip_sil 123456789")

# Kullanıcı hareket loglama
def log_user(user_id, action):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if user_id not in user_logs:
        user_logs[user_id] = []
    user_logs[user_id].append(f"[{now}] {action}")

# Botu başlat
print("Bot aktif! Telegram'dan mesaj bekleniyor...")
bot.infinity_polling()
