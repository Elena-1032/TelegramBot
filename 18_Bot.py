import telebot
from config import TOKEN, keys
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    text = 'Для получения результата конвертации одной валюты на другую валюту введите значения через пробел: \n\
    сумма валюта валюта \nСписок доступной валюты для ввода:\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Список валюты, возможной для конвертации.'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', 1])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise APIException('Неверное количество значений ввода.\n')
        amount, quote, base = values
        total_base = CryptoConverter.convert(amount, quote, base)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n{e} /help')
    except Exception as e:#ошибка серверные
        bot.reply_to(message, f'Не удалось обработать команду\n{e} \n /help')
    else:
        text = f'{amount} ед. <{quote}> это {round(total_base, 2)} ед. <{base}>'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
Footer