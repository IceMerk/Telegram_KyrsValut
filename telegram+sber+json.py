import config  # Тут лежит токен от Телеграма
import telebot
import requests
import json
from datetime import datetime

''' Данный бот написан самостоятельно, 
в рамках программы обучения ScillFactory

-----Функции----
def get_kurs() -> True:  Получаем курс валют
def chek_time_kurs() -> True:  Фунция сверки дня, если надо запрашиваем новый json через get_kurs
def chek_valuta(valuta: str) -> str or False:  Сверяем запросы валют и присваеваем как в json
def chek_len(dlina) -> bool:  Проверяем введеный текст на длину
def chek_user(cifra: str) -> bool:  Проверяем на цифру
def text_for_user(vy: str, vs: str, coin: str) -> str:  Печатает текст для пользователя

@bot.message_handler(commands=['start', 'help'])  Приветствие, оно же помощь
@bot.message_handler(commands=['values'])  Смотрим что можем считать в валютах
@bot.message_handler(content_types=['text']) Функция работы с введеным текстом валют
'''


url = 'https://www.cbr-xml-daily.ru/daily_json.js'
bot = telebot.TeleBot(config.TOKEN)
with open('kurs.json') as f:  # Открываем файл курса валют
    file_json = json.load(f)  # Кладем его в переменную


def get_kurs() -> True:  # Получаем курс валют
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        r = requests.get(url).text
        with open('kurs.json', 'w') as file:  # Записываем в файл, чтобы постоянно не запрашивать
            file.write(r)
        return True
    except Exception:  # Если Сервер не доступен
        print('Сервер не доступен')


def chek_time_kurs() -> True:  # Фунция сверки дня, если надо запрашиваем новый json через get_kurs
    time_now = str(datetime.now()).split(' ')[0]
    time_json = file_json['Date'].split('T')[0]
    if time_now != time_json:  # Сверяем дни: локальный и в файле курса валют (можно сделать по часам)
        get_kurs()  # если даты не совпали, то создаем новый
    return True


def chek_valuta(valuta: str) -> str or False:  # Сверяем запросы валют и присваеваем как в json
    usd = ['доллар', 'usd', 'зеленый', 'бакс', 'долар']
    ru = ['рубль', 'ru', 'деревянный', 'рупь', 'целковый']
    cny = ['юань', 'cny', 'китайских']
    eur = ['евро']
    if any([valuta[:3] in x for x in usd]): return 'USD'
    elif any([valuta[:3] in x for x in ru]): return 'RU'
    elif any([valuta[:3] in x for x in cny]): return 'CNY'
    elif any([valuta[:3] in x for x in eur]): return 'EUR'
    return False


def chek_len(dlina) -> bool:  # Проверяем введеный текст на длину
    if dlina != 3:
        return False
    else:
        return True


def chek_user(cifra: str) -> bool:  # Проверяем на цифру
    cifra = cifra.replace(',', '')  # Если есть в тексте точка или запятая - убираем
    cifra = cifra.replace('.', '')
    if not cifra.isnumeric():  # Проверка на цифры в строке
        return False
    else:
        return True


def text_for_user(vy: str, vs: str, coin: str) -> str:  # Печатает текст для пользователя
    coin = float(coin.replace(',', '.'))  # Редактируем цифру, чтобы умножить
    vy_ch, vs_ch = chek_valuta(vy.lower()), chek_valuta(vs.lower())  # Сверяем в валютах и присваеваем нужный знак
    if vy_ch and vs_ch:  # Если не False
        if vs_ch == 'RU':  # В jsone нет рублей, поэтому отдельная проверка на первую валюту
            vy_j = file_json['Valute'][vy_ch]['Value']
            return f'{vy} в переводе на {vs} равен {round(vy_j * coin, 2)}'
        elif vy_ch == 'RU':  # на вторую валюту
            vs_j = file_json['Valute'][vs_ch]['Value']
            return f'{vy} в переводе на {vs} равен {round(vs_j * coin, 2)}'
        elif vy_ch != 'RU' and vs_ch != 'RU':  # Иначе считаем с нужными
            vy_j, vs_j = file_json['Valute'][vy_ch]['Value'], file_json['Valute'][vs_ch]['Value']
            if vy_j > vs_j:
                return f'{vy} в переводе на {vs} равен {round((vy_j - vs_j) * coin, 2)}'
            return f'{vy} в переводе на {vs} равен {round((vs_j - vy_j) * coin, 2)}'
    else:  # Если проверки валют не прошли
        return f'Такой валюты ещё нет. 🙄 Доступные валюты👉 /values'


@bot.message_handler(commands=['start', 'help'])  # Приветствие, оно же помощь
def start_help(message):
    text = 'Тут можно узнать курс одной валюты к другой\n' \
           '<Валюта в которой узнаем> <Валюта для сравнения> <Цифра>\n' \
           'Пример: юань рубль 100\n' \
           'Инструкция: /help\n' \
           'Доступные валюты: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])  # Смотрим что можем считать в валютах
def values(message):
    valuta = ['💵 доллар', '💶 евро', '💴 юань', '💴 рубль']
    text = 'Доступные валюты: '
    for k in valuta:
        text += f'\n{k}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def ask_valuta(message):
    chek_time_kurs()  # Смотрим на актуальность файла валют, если надо грузим новый
    list_text = message.text.split(' ')  # Разбиваем список
    if chek_len(len(list_text)):  # Проверка длины
        if chek_user(list_text[2]):  # Проверка числа
            text = text_for_user(*list_text)  # Распаковываем список в функцию текста
            bot.send_message(message.chat.id, text)
        else:
            text = 'Неверный формат. Шаблон ввода 👉 /help'  # Если не прошли проверку числа
            bot.send_message(message.chat.id, text)
    else:  # Если не прошли проверку длины
        text = 'Неверный формат. Шаблон ввода 👉 /help'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
