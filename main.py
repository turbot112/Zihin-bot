import os
import logging
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # GPT desteği için
GRUP_CHAT_ID = -1002512446830
VIP_USERS = [1769686760, 1121214662]
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662

logging.basicConfig(filename="zihinbot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def is_vip(user_id): return user_id in VIP_USERS
def log_event(text): logging.info(text)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot 5.0'a hoş geldin! Komutlar için /yardim yazabilirsin. Sistem GPT ile gelişiyor.")

def yardim(update: Update, context: CallbackContext):
    komutlar = (
        "/start - Botu başlat\n"
        "/yardim - Komutları göster\n"
        "/coinler - Popüler coin listesi\n"
        "/fiyat <coin> - Anlık fiyat\n"
        "/rsi <coin> - RSI değeri (demo)\n"
        "/analiz <coin> - GPT ile analiz\n"
        "/guncelle - Sürüm kontrol\n"
        "/yenilik - Planlanan yenilikler\n"
        "/log - Son kayıtlar\n"
        "/destek - Destek bildirimi gönder"
    )
    update.message.reply_text(komutlar)

def coinler(update: Update, context: CallbackContext):
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOGEUSDT", "XRPUSDT"]
    buttons = [[InlineKeyboardButton(c, callback_data=f"coin_{c}")] for c in coins]
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Popüler coinleri seç:", reply_markup=markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data.startswith("coin_"):
        coin = query.data.replace("coin_", "")
        try:
            price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}", timeout=5).json()["price"]
            rsi = 42.75
            query.edit_message_text(f"{coin} Fiyat: {price} USDT\nRSI: {rsi}")
            log_event(f"Coin sorgusu: {coin} - {price}")
        except Exception as e:
            query.edit_message_text("Veri alınamadı.")
            log_event(f"HATA - Coin sorgu: {e}")

def fiyat(update: Update, context: CallbackContext):
    try:
        symbol = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5).json()["price"]
        update.message.reply_text(f"{symbol} fiyatı: {price} USDT")
    except Exception as e:
        update.message.reply_text("Fiyat alınamadı.")

def rsi(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        fake_rsi = 42.75
        update.message.reply_text(f"{coin} RSI değeri: {fake_rsi}")
    except:
        update.message.reply_text("Kullanım: /rsi BTCUSDT")

def analiz(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}").json()["price"]
        prompt = f"{coin} şu an {price} USDT seviyesinde işlem görüyor. RSI değeri 42.75. Teknik analiz yap ve öneri ver."
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        response = requests.post(
            "https://api.openai.com/v1/completions",
            json={
                "model": "text-davinci-003",
                "prompt": prompt,
                "temperature": 0.7,
                "max_tokens": 150,
            },
            headers=headers
        )
        reply = response.json()['choices'][0]['text']
        update.message.reply_text(f"{coin} GPT Analizi:\n{reply.strip()}")
    except Exception as e:
        update.message.reply_text("Analiz alınamadı.")
        log_event(f"GPT Analiz hatası: {e}")

def destek(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Destek talebi: {user.id} - @{user.username or 'anonim'}"
    context.bot.send_message(ADMIN_ID, text)
    context.bot.send_message(DESTEK_ID, text)
    update.message.reply_text("Destek talebin alındı.")

def guncelle(update: Update, context: CallbackContext):
    update.message.reply_text("Yeni özellikler kontrol ediliyor...")

def yenilik(update: Update, context: CallbackContext):
    update.message.reply_text("Yakında: otomatik sinyal motoru, tam al/sat, abonelik modülü ve daha fazlası.")

def logoku(update: Update, context: CallbackContext):
    try:
        with open("zihinbot.log", "r") as f:
            lines = f.readlines()[-10:]
            update.message.reply_text("Son loglar:\n" + "".join(lines))
    except:
        update.message.reply_text("Log okunamadı.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", yardim))
    dp.add_handler(CommandHandler("coinler", coinler))
    dp.add_handler(CommandHandler("fiyat", fiyat))
    dp.add_handler(CommandHandler("rsi", rsi))
    dp.add_handler(CommandHandler("analiz", analiz))
    dp.add_handler(CommandHandler("guncelle", guncelle))
    dp.add_handler(CommandHandler("yenilik", yenilik))
    dp.add_handler(CommandHandler("log", logoku))
    dp.add_handler(CommandHandler("destek", destek))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
