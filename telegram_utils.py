import telegram

# get id, username: https://api.telegram.org/bot[token]/getUpdates

def send_telegram(photo_path="alert.png"):
    try:
        my_token = "5655634559:AAG0XnbBWyINQZE0KMD1SyeFt3wvRjCwZDM"
        bot = telegram.Bot(token=my_token)
        bot.sendPhoto(chat_id="5175598352", photo=open(photo_path, "rb"), caption="Có xâm nhập, nguy hiểm!")
    except Exception as ex:
        print("Can not send message telegram ", ex)

    print("Send sucess")