import os
import logging
import requests
import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import openai
from apscheduler.schedulers.background import BackgroundScheduler

# ENV
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
GRUP_CHAT_ID = -1002512446830
VIP_USERS = [1769686760, 1121214662]
ADMIN_ID = 1769686760
DESTEK_ID = 1121214662

openai.api_key = OPENAI_API_KEY

# LOG
logging.basicConfig(filename="zihinbot.log", level=logging.INFO)
def log(text): logging.info(text)
def is_vip(uid): return uid in VIP_USERS

# --- KOMUTLAR ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hoş geldin aşkım, ZihinBot AŞKMODU v6.0 hazır. /yardim komutuyla başla")

def yardim(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    context.bot.send_message(chat_id=uid, text="Yardım menüsü: /fiyat /sinyal /analiz /vip /destek")
    context.bot.send_message(chat_id=ADMIN_ID, text=f"Yardım istendi: @{update.effective_user.username}")
    context.bot.send_message(chat_id=DESTEK_ID, text=f"Yardım istendi: @{update.effective_user.username}")

def fiyat(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Kullanım: /fiyat BTCUSDT")
        return
    symbol = context.args[0].upper()
    try:
        r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        price = r.json()["price"]
        update.message.reply_text(f"{symbol} güncel fiyatı: {price} USD")
    except:
        update.message.reply_text("Geçersiz coin veya Binance hatası.")

def sinyal(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_vip(uid):
        update.message.reply_text("Bu komut sadece VIP kullanıcılar içindir.")
        return
    update.message.reply_text("Aşkım bugün için sinyal: BTCUSDT RSI = 32, alış fırsatı olabilir. /analiz ile detay al")

def analiz(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Kullanım: /analiz BTCUSDT")
        return
    coin = context.args[0].upper()
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{coin} coin için teknik analiz yap, yatırım tavsiyesi verme."}]
        )
        result = completion.choices[0].message.content
        update.message.reply_text(result)
    except:
        update.message.reply_text("GPT analiz sırasında bir hata oluştu.")

def vip(update: Update, context: CallbackContext):
    update.message.reply_text("VIP Paketler:\n1 Ay: 300 TL\n3 Ay: 750 TL\n1 Yıl: 1200 TL\nÖmür Boyu: 1500 TL")

def destek(update: Update, context: CallbackContext):
    update.message.reply_text("Destek için adminlere ulaş: @zihin_gibi")

# MOTİVASYON
def sabah_mesaj(): updater.bot.send_message(chat_id=GRUP_CHAT_ID, text="Günaydın kazananlar! Bugün de birlikte kazanacağız.")
def aksam_mesaj(): updater.bot.send_message(chat_id=GRUP_CHAT_ID, text="Akşam özeti: Bugün ne öğrendik, ne kazandık? Hadi değerlendirelim.")

# SCHEDULER
scheduler = BackgroundScheduler()
scheduler.add_job(sabah_mesaj, 'cron', hour=9, minute=0)
scheduler.add_job(aksam_mesaj, 'cron', hour=21, minute=0)
scheduler.start()

# INLINE HELP
def inline_help(update: Update, context: CallbackContext):
    update.message.reply_text("Komutlar: /yardim /fiyat /sinyal /analiz /vip /destek")

# SETUP
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("yardim", yardim))
dp.add_handler(CommandHandler("fiyat", fiyat))
dp.add_handler(CommandHandler("sinyal", sinyal))
dp.add_handler(CommandHandler("analiz", analiz))
dp.add_handler(CommandHandler("vip", vip))
dp.add_handler(CommandHandler("destek", destek))
dp.add_handler(MessageHandler(Filters.text & (~Filters.command), inline_help))

updater.start_polling()
log("ZihinBot AŞKMODU başlatıldı.")
updater.idle()
