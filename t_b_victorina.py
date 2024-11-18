from telebot import TeleBot, types
import random

TOKEN = '7596980839:AAEAyGgj5K2s0A7f4IJYUw52WnmiD3nnB6w'

bot = TeleBot(TOKEN)
users = {}

questions = {1: [("В каком году началась Великая Отечественная война?", "1941"),("Кто был первым президентом США?", "Джордж Вашингтон")],
            2: [("Кто был первым императором Римской империи?", "Октавиан Август"),("В каком году распался Советский Союз?", "1991")],
            3: [("Когда была подписана Магна Карта?", "1215"),("Кто был фараоном при строительстве пирамид?", "Хеопс")]}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    users[user_id] = {"name": message.from_user.first_name, "level": None, "points": 0, "current_question": 0,
                      "current_question_info": None}
    bot.send_message(user_id,
                     f"Приветствую тебя, {message.from_user.first_name}! Это викторина по истории. Выбери уровень сложности: 1, 2 или 3.",
                     reply_markup=types.ForceReply(selective=True))

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) == 1 and m.reply_to_message is not None)
def set_level(message):
    user_id = message.from_user.id
    level = int(message.text)
    if level in [1, 2, 3]:
        users[user_id]["level"] = level
        bot.send_message(user_id, f"Твой уровень сложности: {level}. Начнем викторину!")
        ask_question(user_id)
    else:
        bot.send_message(user_id, "Уровень сложности должен быть числом от 1 до 3. Попробуй еще раз:",
                         reply_markup=types.ForceReply(selective=True))

def ask_question(user_id):
    user_data = users[user_id]
    current_question = user_data["current_question"]
    level = user_data["level"]
    question, answer = random.choice(questions[level])
    user_data["current_question_info"] = (question, answer)
    bot.send_message(user_id, f"Вопрос {current_question + 1}: {question}",
                     reply_markup=types.ForceReply(selective=True))

@bot.message_handler(func=lambda m: m.reply_to_message is not None)
def handle_answers(message):
    user_id = message.from_user.id
    user_data = users[user_id]
    current_question = user_data["current_question"]
    question, answer = user_data["current_question_info"]

    user_answer = message.text.strip().lower()
    correct_answer = answer.strip().lower()

    if user_answer == correct_answer:
        user_data["points"] += 1
        bot.send_message(user_id, "Верно!")
    else:
        bot.send_message(user_id, f"Неверно. Правильный ответ: {answer}")
    user_data["current_question"] += 1
    if user_data["current_question"] >= 3:
        finish_quiz(user_id)
    else:
        ask_question(user_id)

def finish_quiz(user_id):
    user_data = users[user_id]
    points = user_data["points"]
    if points == 3:
        bot.send_message(user_id, f"Ты историк!")
    elif points == 2:
        bot.send_message(user_id, f"Хорошо, но нужно глубже изучать..")
    else:
        bot.send_message(user_id, f"История не твоя сильная сторона.")
    del users[user_id]
if __name__ == '__main__':
    bot.polling(non_stop=True)