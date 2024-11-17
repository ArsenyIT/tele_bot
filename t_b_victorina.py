import telebot
from random import choice

# Вставьте сюда ваш токен от BotFather
TOKEN = '7596980839:AAEAyGgj5K2s0A7f4IJYUw52WnmiD3nnB6w'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет! Я викторина по истории. Напишите ваше имя.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Обрабатываем сообщение пользователя
    user_name = message.text.strip()
    bot.send_message(message.chat.id, f"{user_name}, выберите уровень сложности (1-3).")

    @bot.message_handler(func=lambda msg: True)
    def handle_level(msg):
        try:
            level = int(msg.text.strip())
        except ValueError:
            level = 1
            bot.send_message(msg.chat.id, 'Установлен первый уровень сложности.')

        if level < 1 or level > 3:
            level = 1
            bot.send_message(msg.chat.id, 'Установлен первый уровень сложности.')

        questions = {
            1: [
                ('В каком году началась Великая Отечественная Война?', "1941"),
                ("Кто был первым президентом США?", "Джордж Вашингтон")
            ],
            2: [
                ('Кто был первым императором Римской Империи?', "Октавиан Август"),
                ("В каком году распался СССР?", "1991")
            ],
            3: [
                ('Когда была подписана Магна Карта?', "1215"),
                ("Кто был фараоном во время строительства пирамид?", "Хеопс")
            ]
        }

        points = 0
        for _ in range(3):
            question, correct_answer = choice(questions[level])
            bot.send_message(msg.chat.id, f"{user_name}, {question}")

            @bot.message_handler(func=lambda m: True)
            def handle_answer(m):
                student_answer = m.text.strip().lower()
                if student_answer == correct_answer.lower():
                    points += 1
                    bot.send_message(m.chat.id, 'Правильно!')
                else:
                    bot.send_message(m.chat.id, f'Неправильно. Правильный ответ: {correct_answer}')

                if points == 3:
                    bot.send_message(m.chat.id, f"Ты историк, {user_name}!")
                elif points == 2:
                    bot.send_message(m.chat.id, f"Хорошо, {user_name}, но нужно глубже изучать.")
                else:
                    bot.send_message(m.chat.id, f"История не твоя сильная сторона, {user_name}.")

                bot.register_next_step_handler(m, handle_answer)

            bot.register_next_step_handler(msg, handle_answer)


bot.polling(none_stop=True)