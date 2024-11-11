import telebot

API_TOKEN = '7596980839:AAEAyGgj5K2s0A7f4IJYUw52WnmiD3nnB6w'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == "привет!":
        bot.reply_to(message, "И тебе всего хорошего!!!")

bot.polling()