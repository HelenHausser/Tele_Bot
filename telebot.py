import telebot
from config import keys, TOKEN
from utils import ConvertionException, get_price

bot = telebot.TeleBot(TOKEN)

# при вводе команд выводим приветствие
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Добро пожаловать, {message.chat.username}!")
    text = "Чтобы начать со мной работу введите команду в следующем формате: \n<имя валюты, цену которой вы хотите узнать> \
\n<имя валюты, в которой надо узнать цену первой валюты> \
\n<количество первой валюты>\nЧтобы увидеть список всех доступных валют нажмите: /values"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} составляет {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
