import os
import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

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
    update.message.reply_text("ZihinBot 4.0'a hoş geldin! /yardim yazabilirsin. Sistem kendini geliştiriyor.")

def yardim(update: Update, context: CallbackContext):
    komutlar = (
        "/start - Botu başlat
"
        "/yardim - Komutları göster
"
        "/coinler - Popüler coin listesi
"
        "/fiyat <coin> - Anlık fiyat
"
        "/rsi <coin> - RSI analizi (demo)
"
        "/güncelle - Yeni sürüm kontrolü
"
        "/yenilik - Planlanan geliştirmeleri göster
"
        "/log - Son 10 hata/gelişme kaydı
"
        "/destek - Destek bildirimi gönder"
    )
    update.message.reply_text(komutlar)

def coinler(update: Update, context: CallbackContext):
    coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'XRPUSDT']
    buttons = [[InlineKeyboardButton(c, callback_data=f"coin_{c}")] for c in coins]
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Popüler coinleri seç:", reply_markup=markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data.startswith("coin_"):
        coin = query.data.replace("coin_", "")
        try:
            response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}", timeout=5)
            price = response.json()["price"]
            rsi = 42.75
            query.edit_message_text(f"{coin} Fiyatı: {price} USDT
RSI: {rsi}")
            log_event(f"Coin sorgusu: {coin} {price}")
        except Exception as e:
            query.edit_message_text("Bilgi alınamadı.")
            log_event(f"HATA - Coin veri çekilemedi: {str(e)}")

def fiyat(update: Update, context: CallbackContext):
    try:
        symbol = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5).json()["price"]
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
    update.message.reply_text("Destek bildirimin gönderildi.")
    log_event(f"Destek talebi alındı: {text}")

def guncelle(update: Update, context: CallbackContext):
    update.message.reply_text("Yeni sürüm kontrol ediliyor...")
    log_event("Güncelleme komutu çalıştı (manuel onay gerekebilir).")

def yenilik(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Planlanan yenilikler:
"
        "- Tam otomatik sinyal motoru
"
        "- TradingView entegrasyonu
"
        "- Favori coin takip sistemi
"
        "- Otomatik al/sat modülü
"
        "- GPT ile içerik üretimi"
    )
    log_event("Yenilikler gösterildi.")

def logoku(update: Update, context: CallbackContext):
    try:
        with open("zihinbot.log", "r") as f:
            lines = f.readlines()[-10:]
            update.message.reply_text("Son loglar:
" + "".join(lines))
    except Exception as e:
        update.message.reply_text("Log okunamadı.")
        log_event(f"Log okuma hatası: {str(e)}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", yardim))
    dp.add_handler(CommandHandler("coinler", coinler))
    dp.add_handler(CommandHandler("fiyat", fiyat))
    dp.add_handler(CommandHandler("rsi", rsi))
    dp.add_handler(CommandHandler("güncelle", guncelle))
    dp.add_handler(CommandHandler("yenilik", yenilik))
    dp.add_handler(CommandHandler("log", logoku))
    dp.add_handler(CommandHandler("destek", destek))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
