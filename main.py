import os
import requests
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Ortam değişkenlerinden bot token'ını al
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GRUP_CHAT_ID = -1002512446830  # Ücretsiz sinyal gönderilecek grup ID

# Kalıcı VIP kullanıcılar
vip_users = [1769686760, 1121214662]

# Admin ve destek
admin_id = 1769686760
destek_id = 1121214662

# VIP kontrol
def is_vip(user_id):
    return user_id in vip_users

# Komut: /start
def start(update, context):
    update.message.reply_text(
        "Hoş geldin kripto savaşçısı!\nKomutlar:\n"
        "/sinyal\n/vipsinyal\n/ozet\n/fiyat BTCUSDT\n/rsi BTCUSDT\n/odeme\n/vip\n/destek"
    )

# Komut: /id
def id_handler(update, context):
    update.message.reply_text(f"Telegram ID: {update.effective_user.id}")

# Komut: /sinyal (gruba gönderilir)
def sinyal_handler(update, context):
    context.bot.send_message(chat_id=GRUP_CHAT_ID, text="Ücretsiz Sinyal: BTC/USDT 10x Long\nGiriş: 62.000\nTP: 63.800\nSL: 61.000")

# Komut: /vipsinyal
def vipsinyal_handler(update, context):
    user_id = update.effective_user.id
    if is_vip(user_id):
        context.bot.send_message(chat_id=user_id, text="VIP Sinyal: ETH/USDT 20x Long\nGiriş: 3.100\nTP: 3.250\nSL: 2.950")
    else:
        update.message.reply_text("Bu sinyal VIP üyeler içindir. /odeme komutunu kullanabilirsin.")

# Komut: /ozet
def ozet_handler(update, context):
    user_id = update.effective_user.id
    if is_vip(user_id):
        context.bot.send_message(chat_id=user_id, text="Günlük Kazanç Özeti:\n- BTC: +6.2%\n- ETH: +3.1%\n- SOL: +8.9%")
    else:
        update.message.reply_text("Bu özet sadece VIP üyeler içindir.")

# Komut: /fiyat
def fiyat_handler(update, context):
    try:
        symbol = context.args[0].upper()
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        data = requests.get(url).json()
        update.message.reply_text(f"{symbol} fiyatı: {data['price']} USDT")
    except:
        update.message.reply_text("Kullanım: /fiyat BTCUSDT")

# Komut: /rsi
def rsi_handler(update, context):
    try:
        coin = context.args[0].upper()
        fake_rsi = 42.75
        update.message.reply_text(f"{coin} için RSI değeri: {fake_rsi}")
    except:
        update.message.reply_text("Kullanım: /rsi BTCUSDT")

# Komut: /odeme
def odeme_handler(update, context):
    update.message.reply_text(
        "VIP Üyelik Ödeme Bilgileri:\n"
        "- Papara: 1492701376\n"
        "- 1 Ay: 300 TL\n- 3 Ay: 750 TL\n- 1 Yıl: 1200 TL\n- Ömür Boyu: 1500 TL\n\n"
        "Form: https://docs.google.com/forms/d/e/1FAIpQLScXsoYjvQWewMIJFOenljRpdl3LqwnbkGPNjmIrAWeL195fHA/viewform"
    )

# Komut: /vip
def vip_handler(update, context):
    update.message.reply_text(
        "VIP ile kazan:\n- Özel sinyaller\n- Günlük özet\n- RSI analiz\n- Otomatik işlem desteği\n"
        "VIP olmak için: /odeme"
    )

# Komut: /destek
def destek_handler(update, context):
    user = update.effective_user
    text = f"Destek talebi: {user.id} - @{user.username}"
    context.bot.send_message(chat_id=admin_id, text=text)
    context.bot.send_message(chat_id=destek_id, text=text)
    update.message.reply_text("Destek isteğin alındı. Ekibimiz yakında seninle ilgilenecek.")

# Komut: /vip_ekle
def vip_ekle_handler(update, context):
    if update.effective_user.id != admin_id:
        return
    try:
        new_id = int(context.args[0])
        if new_id not in vip_users:
            vip_users.append(new_id)
            update.message.reply_text(f"{new_id} artık VIP.")
        else:
            update.message.reply_text("Zaten VIP.")
    except:
        update.message.reply_text("Kullanım: /vip_ekle 123456789")

# Komut: /vip_sil
def vip_sil_handler(update, context):
    if update.effective_user.id != admin_id:
        return
    try:
        sil_id = int(context.args[0])
        if sil_id in vip_users:
            vip_users.remove(sil_id)
            update.message.reply_text(f"{sil_id} VIP listesinden çıkarıldı.")
        else:
            update.message.reply_text("Bu kullanıcı VIP değil.")
    except:
        update.message.reply_text("Kullanım: /vip_sil 123456789")

# Botu başlat
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
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
    dp.add_handler(CommandHandler("vip_ekle", vip_ekle_handler))
    dp.add_handler(CommandHandler("vip_sil", vip_sil_handler))

    print("Zihin Bot v2.0 başlatıldı!")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
