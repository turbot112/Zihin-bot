import telegram

BOT_TOKEN = '7526727217:AAFFO1jo-RO72CwKt_Gai6-iY-wC-wSAJhc'
CHAT_ID = -1004634117873  # Grup chat ID (başında -100 olmalı)

bot = telegram.Bot(token=BOT_TOKEN)

def test_sinyal_gonder():
    mesaj = "Test Sinyali: BTC/USDT 10x LONG\nGiriş: 62,000\nHedef: 63,800\nStop: 60,800"
    bot.send_message(chat_id=CHAT_ID, text=mesaj)

# Bu satır çalışınca mesaj gider
test_sinyal_gonder()
