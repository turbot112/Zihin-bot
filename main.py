import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import openai

# --- ENV CONFIG ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GRUP_CHAT_ID = -1002512446830
VIP_USERS = [1769686760, 1121214662]
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662

# --- Logging ---
logging.basicConfig(filename="zihinbot.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
def log(text): logging.info(text)
def is_vip(uid): return uid in VIP_USERS

# --- START & YARDIM ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot 5.5 Ultimate hazır! /yardim yazarak tüm komutları görebilirsin.")

def yardim(update: Update, context: CallbackContext):
    komutlar = (
        "/start - Botu başlat\n"
        "/yardim - Komutları göster\n"
        "/coinler - Coin seçimi\n"
        "/fiyat <COIN> - Fiyat göster\n"
        "/rsi <COIN> - RSI değeri (demo)\n"
        "/analiz <COIN> - GPT ile analiz\n"
        "/sinyal - Ücretsiz sinyal (grup)\n"
        "/vipsinyal - VIP sinyal\n"
        "/ozet - Günlük özet (VIP)\n"
        "/guncelle - Sürüm bilgisi\n"
        "/yenilik - Planlananlar\n"
        "/log - Son 10 log\n"
        "/destek - Admin’e mesaj"
    )
    update.message.reply_text(komutlar)

# --- COIN BUTTONS ---
def coinler(update: Update, context: CallbackContext):
    coins = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]
    buttons = [[InlineKeyboardButton(coin, callback_data=f"coin_{coin}")] for coin in coins]
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Hızlı coin seçimi:", reply_markup=markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    coin = query.data.replace("coin_", "")
    try:
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}").json()['price']
        query.edit_message_text(f"{coin} → {price} USDT\nRSI: 42.75")
    except:
        query.edit_message_text("Coin bilgisi alınamadı.")

# --- KOMUTLAR ---
def fiyat(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}").json()['price']
        update.message.reply_text(f"{coin} fiyatı: {price} USDT")
    except:
        update.message.reply_text("Fiyat alınamadı.")

def rsi(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        update.message.reply_text(f"{coin} RSI (örnek): 42.75")
    except:
        update.message.reply_text("Kullanım: /rsi BTCUSDT")

def analiz(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}").json()['price']
        openai.api_key = OPENAI_API_KEY
        prompt = f"{coin} fiyatı {price} USDT. RSI 42.75. Teknik analiz önerisi ver."
        gpt = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=150)
        update.message.reply_text(f"{coin} GPT Analizi:\n{gpt['choices'][0]['text'].strip()}")
    except Exception as e:
        update.message.reply_text("Analiz alınamadı.")
        log(f"Analiz hatası: {str(e)}")

def sinyal(update: Update, context: CallbackContext):
    if update.message.chat_id == GRUP_CHAT_ID:
        update.message.reply_text("Ücretsiz Sinyal:\nBTC/USDT 10x LONG\nGiriş: 62000\nTP: 63800\nSL: 61000")
    else:
        update.message.reply_text("Bu komut sadece grupta çalışır.")

def vipsinyal(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if is_vip(uid):
        update.message.reply_text("VIP Sinyal:\nETH/USDT 20x LONG\nGiriş: 3100\nTP: 3250\nSL: 2950")
    else:
        update.message.reply_text("Bu komut sadece VIP üyeler içindir.")

def ozet(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if is_vip(uid):
        update.message.reply_text("Günlük Özeti:\nBTC +6.2%\nETH +4.1%\nSOL +8.9%")
    else:
        update.message.reply_text("Bu komut sadece VIP üyeler içindir.")

def destek(update: Update, context: CallbackContext):
    user = update.effective_user
    mesaj = f"Destek Talebi: {user.id} @{user.username or 'anonim'}"
    context.bot.send_message(chat_id=ADMIN_ID, text=mesaj)
    context.bot.send_message(chat_id=DESTEK_ID, text=mesaj)
    update.message.reply_text("Destek talebin gönderildi.")

def guncelle(update: Update, context: CallbackContext):
    update.message.reply_text("Sistem güncel. Sürüm: 5.5 Ultimate")

def yenilik(update: Update, context: CallbackContext):
    update.message.reply_text("- Otomatik Sinyal\n- API Takibi\n- GPT Analizi\n- Inline Komutlar\n- Grup/Özel Ayrımı")

def logoku(update: Update, context: CallbackContext):
    try:
        with open("zihinbot.log", "r") as f:
            son = f.readlines()[-10:]
            update.message.reply_text("Son loglar:\n" + "".join(son))
    except:
        update.message.reply_text("Log okunamadı.")

# --- MAIN ---
def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("yardim", yardim))
    dp.add_handler(CommandHandler("coinler", coinler))
    dp.add_handler(CommandHandler("fiyat", fiyat))
    dp.add_handler(CommandHandler("rsi", rsi))
    dp.add_handler(CommandHandler("analiz", analiz))
    dp.add_handler(CommandHandler("sinyal", sinyal))
    dp.add_handler(CommandHandler("vipsinyal", vipsinyal))
    dp.add_handler(CommandHandler("ozet", ozet))
    dp.add_handler(CommandHandler("guncelle", guncelle))
    dp.add_handler(CommandHandler("yenilik", yenilik))
    dp.add_handler(CommandHandler("log", logoku))
    dp.add_handler(CommandHandler("destek", destek))
    dp.add_handler(CallbackQueryHandler(button_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
