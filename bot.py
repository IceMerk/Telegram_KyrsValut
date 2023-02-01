import config  # Тут лежит токен от Телеграма
import telebot
import requests
import json
from datetime import datetime

url = 'https://www.cbr-xml-daily.ru/daily_json.js'
bot = telebot.TeleBot(config.TOKEN)

valuta = {
    'доллар': 'USD',
    'евро': 'EUR',
    'юань': 'CNY',
}


def get_kurs():  # Получаем курс валют
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    with open('kurs.json', 'w') as file:  # Записываем в файл, чтобы постоянно не запрашивать
        file.write(requests.get(url).text)
    return True


def open_kurs():
    with open('kurs.json') as f:  # Открываем файл курса валют
        file_json = json.load(f)  # Кладем его в переменную
        time_now = str(datetime.now()).split(' ')[0]
        time_json = file_json['Date'].split('T')[0]
        if time_now != time_json:  # Сверяем дни: локальный и в файле курса валют (можно сделать по часам)
            get_kurs()  # если даты не совпали, то создаем новый
    return file_json


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    text = 'Тут можно узнать курс одной валюты к другой\n' \
           '<Валюта в которой узнаем> <Валюта для сравнения> <Цифра>\n' \
           'Инструкция: /help\n' \
           'Доступные валюты: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты: '
    for k in valuta.keys():
        text += f'\n{k}'
    bot.send_message(message.chat.id, text)


# @bot.message_handler(content_types=['text'])
# def eho(message):
#     bot.reply_to(message, 'Это сообщение обработчика')
#
#
# @bot.message_handler(content_types=['photo'])
# def eho(message):
#     bot.reply_to(message, 'Nice meme XDD')


def main():
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
