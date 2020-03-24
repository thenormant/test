import telebot
import requests
from telebot import types
import sqlite3
import datetime
import urllib



connect = sqlite3.connect('database.db')

cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visit(
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id integer,
    date date,
    time text
    )
""")

connect.commit()
connect.close()

token = "547082437:AAG3j1Ow7YGofsDdnCGPDcpS0Ui8Z3rfHY0"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def say_hello(message):

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    user_id = message.from_user.id

    last_visits = cursor.execute("""
        SELECT *
        FROM visit
        WHERE user_id = (?)
        ORDER BY id DESC
    """, [user_id]).fetchall()

    if len(last_visits) != 0:
        reply_text = f"Привет! Последний раз вы заходили {last_visits[0][2]}"
    else:
        reply_text = 'Hello new user!'
    time = datetime.datetime.now()
    date = datetime.date.today()

    cursor.execute("""
        INSERT INTO visit (user_id, date)
        VALUES (?, ?)
    """, [user_id, time])

    connect.commit()
    connect.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/start')
    btn2 = types.KeyboardButton('/valute')
    btn3 = types.KeyboardButton('/randomText')

    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

@bot.message_handler(commands=['randomText'])
def printRandomText(message):
    bot.send_message(message.chat.id, "This text is random. Trust me.")

@bot.message_handler(commands=['космос'])
def reply_space(message):
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    data = requests.get(url).json()

    print(data)




@bot.message_handler(commands=['valute'])
def get_valute(message):
    data = requests.get("https://www.cbr-xml-daily.ru/daily_json.js").json()
    usd = data['Valute']['USD']['Value']
    eur = data['Valute']['EUR']['Value']
    bot.send_message(message.chat.id, f"USD = {usd}, EUR = {eur}")

@bot.message_handler(regexp='привет')
def reply_to_hello(message):
    bot.send_message(message.chat.id, f"О, привет, {message.from_user.first_name}! А я тебя знаю!")

@bot.message_handler(content_types=['text'])
def reply_to_text(message):
    text = message.text
    bot.send_message(message.chat.id, f"Вы написали {text}, я пока не умею обрабатывать такую команду")


bot.polling()