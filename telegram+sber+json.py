import config  # Тут лежит токен от Телеграма
import telebot
import requests
import json
from datetime import datetime

url = 'https://www.cbr-xml-daily.ru/daily_json.js'
bot = telebot.TeleBot(config.TOKEN)


def get_kurs() -> True:  # Получаем курс валют
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        r = requests.get(url).text
        with open('kurs.json', 'w') as file:  # Записываем в файл, чтобы постоянно не запрашивать
            file.write(r)
        return True
    except:
        Exception('Сервер не доступен')


def chek_time_kurs() -> True:
    time_now = str(datetime.now()).split(' ')[0]
    time_json = file_json['Date'].split('T')[0]
    if time_now != time_json:  # Сверяем дни: локальный и в файле курса валют (можно сделать по часам)
        get_kurs()  # если даты не совпали, то создаем новый
    return True


with open('kurs.json') as f:  # Открываем файл курса валют
    file_json = json.load(f)  # Кладем его в переменную


def chek_valuta(valuta: str) -> str or False:
    usd = ['доллар', 'usd', 'зеленый', 'бакс', 'долар']
    ru = ['рубль', 'ru', 'деревянный', 'рупь', 'целковый']
    cny = ['юань', 'cny', 'китайских']
    eur = ['евро']
    if any([valuta[:3] in x for x in usd]): return 'USD'
    elif any([valuta[:3] in x for x in ru]): return 'RU'
    elif any([valuta[:3] in x for x in cny]): return 'CNY'
    elif any([valuta[:3] in x for x in eur]): return 'EUR'
    return False


def chek_user(dlina: int, cifra: str) -> bool:
    if dlina != 3:
        return False
    elif not cifra.isnumeric():
        return False
    else:
        return True


def text_for_user(vy: str, vs: str, coin: str) -> str:
    vy_ch, vs_ch = chek_valuta(vy), chek_valuta(vs)
    coin = float(coin.replace(',', '.'))
    if vs_ch == 'RU':
        vy_j = file_json['Valute'][vy_ch]['Value']
        return f'{vy} в переводе на {vs} равен {round(vy_j * coin, 2)}'
    elif vy_ch == 'RU':
        vs_j = file_json['Valute'][vs_ch]['Value']
        return f'{vy} в переводе на {vs} равен {round(vs_j * coin, 2)}'
    else:
        vy_j, vs_j = file_json['Valute'][vy_ch]['Value'], file_json['Valute'][vs_ch]['Value']
        if vy_j > vs_j:
            return f'{vy} в переводе на {vs} равен {round((vy_j - vs_j) * coin, 2)}'
        return f'{vy} в переводе на {vs} равен {round((vs_j - vy_j) * coin, 2)}'


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    text = 'Тут можно узнать курс одной валюты к другой\n' \
           '<Валюта в которой узнаем> <Валюта для сравнения> <Цифра>\n' \
           'Инструкция: /help\n' \
           'Доступные валюты: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message):
    valuta = {
        'доллар': 'USD',
        'евро': 'EUR',
        'юань': 'CNY',
    }
    text = 'Доступные валюты: '
    for k in valuta.keys():
        text += f'\n{k}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def ask_valuta(message):
    chek_time_kurs()
    list_text = message.text.split(' ')

    if not chek_user(len(list_text), list_text[2]):
        text = 'Что-то не то с цифрой'
        bot.send_message(message.chat.id, text)
    else:
        text = text_for_user(*list_text)
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
