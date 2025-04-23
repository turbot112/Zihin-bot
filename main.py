import os
import requests
import telebot
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Gruptaki ücretsiz sinyal gönderilecek chat ID
GRUP_CHAT_ID = -1002512446830

# Kalıcı VIP kullanıcılar
vip_users = [1769686760, 1121214662]

# Admin ve destek bildirimi
admin_id = 1769686760
destek_id = 1121214662

# VIP kontrolü
def is_vip(user_id):
    return user_id in vip_users

# /start komutu
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Hoş geldin kripto savaşçısı! Komutlar: /sinyal /vipsinyal /ozet /fiyat /rsi /odeme /vip /destek")

# /id komutu
@bot.message_handler(commands=['id'])
def id_handler(message):
    bot.reply_to(message, f"Telegram ID: {message.from_user.id}")

# /sinyal → gruptan herkese açık
@bot.message_handler(commands=['sinyal'])
def sinyal_handler(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "Bu komut sadece grupta kullanılabilir.")
        return
    bot.send_message(GRUP_CHAT_ID, "Ücretsiz Sinyal: BTC/USDT 10x Long\nGiriş: 62.000\nTP: 63.800\nSL: 61.000")

# /vipsinyal → sadece VIP’lere özelden
@bot.message_handler(commands=['vipsinyal'])
def vipsinyal_handler(message):
    if is_vip(message.from_user.id):
        bot.send_message(message.from_user.id, "VIP Sinyal: ETH/USDT 20x Long\nGiriş: 3.100\nTP: 3.250\nSL: 2.950")
    else:
        bot.send_message(message.chat.id, "Bu sinyal VIP üyeler içindir. /odeme komutunu kullanabilirsin.")

# /ozet → sadece VIP'lere özel
@bot.message_handler(commands=['ozet'])
def ozet_handler(message):
    if is_vip(message.from_user.id):
        bot.send_message(message.from_user.id, "Günlük Kazanç Özeti:\n- BTC: +6.2%\n- ETH: +3.1%\n- SOL: +8.9%")
    else:
        bot.send_message(message.chat.id, "Bu özet sadece VIP üyeler içindir.")

# /fiyat <coin> → canlı fiyat
@bot.message_handler(commands=['fiyat'])
def fiyat_handler(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Kullanım: /fiyat BTCUSDT")
        return
    try:
        symbol = parts[1].upper()
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        data = requests.get(url).json()
        bot.send_message(message.chat.id, f"{symbol} fiyatı: {data['price']} USDT")
    except:
        bot.send_message(message.chat.id, "Fiyat alınamadı.")

# /rsi <coin> → RSI değeri (fake değer veriyoruz şimdilik)
@bot.message_handler(commands=['rsi'])
def rsi_handler(message):
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(message.chat.id, "Kullanım: /rsi BTCUSDT")
        return
    coin = parts[1].upper()
    fake_rsi = 42.75
    bot.send_message(message.chat.id, f"{coin} için RSI değeri: {fake_rsi}")

# /odeme → ödeme ve form bilgisi
@bot.message_handler(commands=['odeme'])
def odeme_handler(message):
    bot.send_message(message.chat.id, 
        "VIP Üyelik Ödeme Bilgileri:\n"
        "- Papara: 1492701376\n"
        "- 1 Ay: 300 TL\n- 3 Ay: 750 TL\n- 1 Yıl: 1200 TL\n- Ömür Boyu: 1500 TL\n\n"
        "Formu doldur: https://docs.google.com/forms/d/e/1FAIpQLScXsoYjvQWewMIJFOenljRpdl3LqwnbkGPNjmIrAWeL195fHA/viewform")

# /vip → avantajları anlat
@bot.message_handler(commands=['vip'])
def vip_handler(message):
    bot.send_message(message.chat.id,
        "VIP ile kazan:\n- Özel sinyaller\n- Günlük özet\n- RSI analiz\n- Otomatik işlem desteği\n"
        "VIP olmak için: /odeme")

# /destek → admin ve destek ID'ye bildirim
@bot.message_handler(commands=['destek'])
def destek_handler(message):
    text = f"Destek talebi: {message.from_user.id} - @{message.from_user.username}"
    bot.send_message(admin_id, text)
    bot.send_message(destek_id, text)
    bot.send_message(message.chat.id, "Destek isteğin alındı. Ekibimiz yakında seninle ilgilenecek.")

# /vip_ekle ve /vip_sil → sadece admin
@bot.message_handler(commands=['vip_ekle'])
def vip_ekle(message):
    if message.from_user.id != admin_id:
        return
    try:
        new_id = int(message.text.split()[1])
        if new_id not in vip_users:
            vip_users.append(new_id)
            bot.send_message(message.chat.id, f"{new_id} artık VIP.")
        else:
            bot.send_message(message.chat.id, "Zaten VIP.")
    except:
        bot.send_message(message.chat.id, "Kullanım: /vip_ekle 123456789")

@bot.message_handler(commands=['vip_sil'])
def vip_sil(message):
    if message.from_user.id != admin_id:
        return
    try:
        sil_id = int(message.text.split()[1])
        if sil_id in vip_users:
            vip_users.remove(sil_id)
            bot.send_message(message.chat.id, f"{sil_id} VIP listesinden çıkarıldı.")
        else:
            bot.send_message(message.chat.id, "Bu kullanıcı VIP değil.")
    except:
        bot.send_message(message.chat.id, "Kullanım: /vip_sil 123456789")

# Botu çalıştır
print("Zihin Bot v2.0 başlatıldı!")
bot.infinity_polling()
