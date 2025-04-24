import os
import requests
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GRUP_CHAT_ID = -1002512446830
VIP_USERS = [1769686760, 1121214662]
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662

logging.basicConfig(filename="zihinbot.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_vip(user_id):
    return user_id in VIP_USERS

def log_event(text):
    logging.info(text)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot Geliştirici Sürümüne Hoş Geldin! /yardim yaz")

def yardim(update: Update, context: CallbackContext):
    komutlar = (
        "/start - Botu başlat"
"
        "/coinler - Popüler coin listesi
"
        "/fiyat <coin> - Anlık fiyat
"
        "/rsi <coin> - RSI analizi
"
        "/güncelle - Botu güncelle
"
        "/yenilik - Yeni önerileri gör
"
        "/log - Son logları oku
"
        "/destek - Admin desteği al"
    )
    update.message.reply_text(komutlar)

def coinler(update: Update, context: CallbackContext):
    coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'XRPUSDT']
    buttons = [[InlineKeyboardButton(c, callback_data=f"coin_{c}")] for c in coins]
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Coin Seç:", reply_markup=markup)

def fiyat(update: Update, context: CallbackContext):
    try:
        symbol = context.args[0].upper()
        res = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5)
        price = res.json()["price"]
        update.message.reply_text(f"{symbol} fiyatı: {price} USDT")
        log_event(f"Fiyat sorgusu: {symbol} → {price}")
    except Exception as e:
        update.message.reply_text("Fiyat alınamadı.")
        log_event(f"HATA: Fiyat sorgusu - {str(e)}")

def rsi(update: Update, context: CallbackContext):
    try:
        symbol = context.args[0].upper()
        fake_rsi = 42.75
        update.message.reply_text(f"{symbol} RSI değeri: {fake_rsi}")
        log_event(f"RSI sorgusu: {symbol} → {fake_rsi}")
    except Exception as e:
        update.message.reply_text("RSI alınamadı.")
        log_event(f"HATA: RSI sorgusu - {str(e)}")

def destek(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Destek talebi: {user.id} - @{user.username or 'anonim'}"
    context.bot.send_message(ADMIN_ID, text)
    context.bot.send_message(DESTEK_ID, text)
    update.message.reply_text("Destek isteğin gönderildi.")
    log_event(f"Destek talebi: {text}")

def guncelle(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot güncelleniyor...
(Yeni sürüm yakında aktif olacak!)")
    log_event("Güncelleme komutu alındı. (Simüle)")

def yenilik(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Yeni öneriler:
"
        "- Favori coin ekleme
"
        "- Fiyat alarm sistemi
"
        "- Kullanıcı paneli
"
        "- RSI tabanlı otomatik sinyal üretimi
"
        "- TradingView entegrasyonu (planlanıyor)"
    )
    log_event("Yenilik komutu çalıştı.")

def logoku(update: Update, context: CallbackContext):
    try:
        with open("zihinbot.log", "r") as f:
            logs = f.readlines()[-10:]
            update.message.reply_text("Son 10 log:
" + "".join(logs))
    except:
        update.message.reply_text("Log okunamadı.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", yardim))
    dp.add_handler(CommandHandler("coinler", coinler))
    dp.add_handler(CommandHandler("fiyat", fiyat))
    dp.add_handler(CommandHandler("rsi", rsi))
    dp.add_handler(CommandHandler("destek", destek))
    dp.add_handler(CommandHandler("güncelle", guncelle))
    dp.add_handler(CommandHandler("yenilik", yenilik))
    dp.add_handler(CommandHandler("log", logoku))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
