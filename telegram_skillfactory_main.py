import telebot
from extensions import APIException, Converted
from config import valuta, TOKEN

''' Данный бот написан с помощью платформы, 
в рамках программы обучения ScillFactory.
Немного дополнен и украшен. Можно немного ошибаться в написани валюты

---Файлы---
telegram_skillfactory_main - основная логика взаимодействия с телеграмом
config - хранит 2 переменные: valuta, TOKEN
extensions - содержит 2 класса: APIException, Converted
-----Классы----
APIException - Исключение
Converted - Проверка данных на правильность, взаимодействие с API (https://apilayer.com/)
            --Функции--: chek_valuta и get_price
---config.valuta---
valuta = {
            'USD': ['доллар', 'usd', 'зеленый', 'бакс', 'долар'],
            'RUB': ['рубль', 'ru', 'деревянный', 'рупь', 'целковый'],
            'CNY': ['юань', 'cny', 'китайских'],
            'EUR': ['евро'],
        }

Вывод: Данный способ легче, проще и красивее, чем самостоятельный telegram+sber+json.
Легко можно расширить список валют. Но нельзя ошибаться в написании, хоть на символ.
Либо делать проверку
'''

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])  # Приветствие, оно же помощь
def start_help(message):
    text = 'Тут можно узнать курс одной валюты к другой\n' \
           '<Валюта> <в какую Валюту перевести> <Цифра>\n' \
           'Пример: юань рубль 100\n' \
           'Инструкция: /help\n' \
           'Доступные валюты: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])  # Смотрим что можем считать в валютах
def values(message):
    text = 'Доступные валюты: '
    for k in valuta.keys():
        text += f'\n{k}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def massege_valuta(message: telebot.types.Message):
    valuta = message.text.split(' ')
    try:
        if len(valuta) != 3:
            raise APIException('❌ Нужно 3 параметра ❌\nПосмотри инструкцию: /help')
        base, quote, amount = valuta
        text = Converted.get_price(base.lower(), quote.lower(), amount)
    except APIException as e:
        bot.reply_to(message, f'{e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling()
