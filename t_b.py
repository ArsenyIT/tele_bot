import telebot

API_TOKEN = '7596980839:AAEAyGgj5K2s0A7f4IJYUw52WnmiD3nnB6w'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: True)
def send_greeting(message):
    bot.reply_to(message, "Привет! И тебе всего хорошего!!!")

if __name__ == '__main__':
    bot.polling()