import config
import telebot

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help(message):
    bot.send_message(message.chat.id, f'Добро пожаловать \ c{message.chat.username}')

@bot.message_handler(content_types=['text'])
def eho(message):
    bot.reply_to(message, 'Это сообщение обработчика')

@bot.message_handler(content_types=['photo'])
def eho(message):
    bot.reply_to(message, 'Nice meme XDD')


bot.polling(none_stop=True)