# ZihinBot 3.0 — Kusursuz Güvenlik ve Performans

import os
import logging
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext

# LOG ayarı
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Ortam değişkenleri
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GRUP_CHAT_ID = -1002512446830
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662
VIP_USERS = [1769686760, 1121214662]

# VIP kontrolü
def is_vip(user_id):
    return user_id in VIP_USERS

# Hata loglama
def error_handler(update: object, context: CallbackContext):
    logger.error(msg="Hata oluştu:", exc_info=context.error)
    try:
        if update and update.effective_user:
            context.bot.send_message(chat_id=update.effective_user.id,
                                     text="Bir hata oluştu. Lütfen tekrar deneyin veya /destek yazın.")
    except Exception as e:
        logger.warning("Kullanıcıya hata bildirimi gönderilemedi: %s", e)

# Komutlar
def start(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot 3.0’a hoş geldin! Komutlar: /sinyal /vipsinyal /ozet /fiyat <coin> /rsi <coin> /odeme /vip /destek")

def id_handler(update: Update, context: CallbackContext):
    update.message.reply_text(f"Telegram ID: {update.effective_user.id}")

def sinyal_handler(update: Update, context: CallbackContext):
    try:
        context.bot.send_message(chat_id=GRUP_CHAT_ID, text="Ücretsiz Sinyal: BTC/USDT 10x Long\nGiriş: 62.000\nTP: 63.800\nSL: 61.000")
    except Exception as e:
        logger.warning("Sinyal gönderilemedi: %s", e)

def vipsinyal_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if is_vip(user_id):
        context.bot.send_message(chat_id=user_id, text="VIP Sinyal: ETH/USDT 20x Long\nGiriş: 3.100\nTP: 3.250\nSL: 2.950")
    else:
        update.message.reply_text("Bu sinyal VIP üyeler içindir. /odeme komutunu kullanabilirsin.")

def ozet_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if is_vip(user_id):
        context.bot.send_message(chat_id=user_id, text="Günlük Kazanç Özeti:\n- BTC: +6.2%\n- ETH: +3.1%\n- SOL: +8.9%")
    else:
        update.message.reply_text("Bu özet sadece VIP üyeler içindir.")

def fiyat_handler(update: Update, context: CallbackContext):
    try:
        if not context.args:
            update.message.reply_text("Kullanım: /fiyat BTCUSDT")
            return
        symbol = context.args[0].upper()
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        price = response.json().get("price", "Bilinmiyor")
        update.message.reply_text(f"{symbol} fiyatı: {price} USDT")
    except Exception as e:
        logger.error("Fiyat sorgusu hatası: %s", e)
        update.message.reply_text("Fiyat alınamadı. Doğru coin kodu girdiğinden emin ol.")

def rsi_handler(update: Update, context: CallbackContext):
    try:
        if not context.args:
            update.message.reply_text("Kullanım: /rsi BTCUSDT")
            return
        coin = context.args[0].upper()
        fake_rsi = 42.75
        update.message.reply_text(f"{coin} için RSI değeri (demo): {fake_rsi}")
    except Exception as e:
        logger.error("RSI hatası: %s", e)
        update.message.reply_text("RSI hesaplanamadı.")

def odeme_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        "VIP Üyelik Ödeme Bilgileri:\n"
        "- Papara: 1492701376\n"
        "- 1 Ay: 300 TL\n- 3 Ay: 750 TL\n- 1 Yıl: 1200 TL\n- Ömür Boyu: 1500 TL\n\n"
        "Form: https://docs.google.com/forms/d/e/1FAIpQLScXsoYjvQWewMIJFOenljRpdl3LqwnbkGPNjmIrAWeL195fHA/viewform"
    )

def vip_handler(update: Update, context: CallbackContext):
    update.message.reply_text("VIP ile kazan:\n- Özel sinyaller\n- Günlük özet\n- RSI analiz\nVIP olmak için: /odeme")

def destek_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Destek talebi: {user.id} - @{user.username or 'isimsiz'}"
    context.bot.send_message(chat_id=ADMIN_ID, text=text)
    context.bot.send_message(chat_id=DESTEK_ID, text=text)
    update.message.reply_text("Destek isteğin alındı. Ekibimiz seninle ilgilenecek.")

# Başlatıcı
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("id", id_handler))
    dp.add_handler(CommandHandler("sinyal", sinyal_handler))
    dp.add_handler(CommandHandler("vipsinyal", vipsinyal_handler))
    dp.add_handler(CommandHandler("ozet", ozet_handler))
    dp.add_handler(CommandHandler("fiyat", fiyat_handler))
    dp.add_handler(CommandHandler("rsi", rsi_handler))
    dp.add_handler(CommandHandler("odeme", odeme_handler))
    dp.add_handler(CommandHandler("vip", vip_handler))
    dp.add_handler(CommandHandler("destek", destek_handler))
    dp.add_error_handler(error_handler)

    print("ZihinBot 3.0 çalışıyor...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
import os
import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GRUP_CHAT_ID = -1002512446830
VIP_USERS = [1769686760, 1121214662]
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

popular_coins = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'DOGEUSDT', 'BNBUSDT']

def is_vip(user_id):
    return user_id in VIP_USERS

def start(update: Update, context: CallbackContext):
    update.message.reply_text("ZihinBot 3.5’a hoş geldin!
Komutlar: /coinler /fiyat BTCUSDT /rsi BTCUSDT /destek /odeme /vip")

def coinler(update: Update, context: CallbackContext):
    buttons = [[InlineKeyboardButton(coin, callback_data=f"coin_{coin}")] for coin in popular_coins]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Popüler Coinler:", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data.startswith("coin_"):
        coin = data.split("_")[1]
        try:
            price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}", timeout=5).json()["price"]
            rsi = 42.75  # Simüle RSI değeri
            query.edit_message_text(f"{coin} Fiyatı: {price} USDT
RSI: {rsi}")
        except:
            query.edit_message_text("Fiyat bilgisi alınamadı.")

def fiyat_handler(update: Update, context: CallbackContext):
    try:
        symbol = context.args[0].upper()
        price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=5).json()["price"]
        update.message.reply_text(f"{symbol} fiyatı: {price} USDT")
    except:
        update.message.reply_text("Fiyat alınamadı veya sembol hatalı.")

def rsi_handler(update: Update, context: CallbackContext):
    try:
        coin = context.args[0].upper()
        fake_rsi = 42.75
        update.message.reply_text(f"{coin} için RSI (demo): {fake_rsi}")
    except:
        update.message.reply_text("Kullanım: /rsi BTCUSDT")

def destek_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    text = f"Destek talebi: {user.id} - @{user.username or 'isimsiz'}"
    context.bot.send_message(chat_id=ADMIN_ID, text=text)
    context.bot.send_message(chat_id=DESTEK_ID, text=text)
    update.message.reply_text("Destek isteğin alındı. Ekibimiz seninle ilgilenecek.")

def odeme_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        "VIP Üyelik Ödeme Bilgileri:
"
        "- Papara: 1492701376
"
        "- 1 Ay: 300 TL
- 3 Ay: 750 TL
- 1 Yıl: 1200 TL
- Ömür Boyu: 1500 TL

"
        "Form: https://docs.google.com/forms/d/e/1FAIpQLScXsoYjvQWewMIJFOenljRpdl3LqwnbkGPNjmIrAWeL195fHA/viewform"
    )

def vip_handler(update: Update, context: CallbackContext):
    update.message.reply_text("VIP ile kazan:
- Özel sinyaller
- Günlük özet
- RSI analiz
VIP olmak için: /odeme")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("coinler", coinler))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(CommandHandler("fiyat", fiyat_handler))
    dp.add_handler(CommandHandler("rsi", rsi_handler))
    dp.add_handler(CommandHandler("destek", destek_handler))
    dp.add_handler(CommandHandler("odeme", odeme_handler))
    dp.add_handler(CommandHandler("vip", vip_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
