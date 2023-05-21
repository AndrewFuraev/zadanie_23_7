import telebot

from config import TOKEN, keys
from extensions import ConvertionExceptions, CurrencyConvertion

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(massege: telebot.types.Message):
    text = 'Чтобы начать работу с ботом необходимо ввести команду в следущем виде:\n <имя валюты>\n<в какую валюту ' \
           'перевести>\n<колличество переводимой валюты>\n Чтобы увидеть список всех доступных валют введите ' \
           'команду: /values\n увидеть эту подсказку: /help или /start'
    bot.reply_to(massege,text)

@bot.message_handler(commands=['values'])
def values(massege: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(massege, text)



@bot.message_handler(content_types=['text', ])
def convert(massege: telebot.types.Message):
    try:
        users_values = massege.text.split(' ')
        if len(users_values) != 3:
            raise ConvertionExceptions('Вы вели больше или меньше трех параметров')

        quote, base, amount = users_values

        n_base = CurrencyConvertion.get_price(quote, base, amount)
    except ConvertionExceptions as e:
        bot.reply_to(massege, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(massege, f'Не удалось обработать команду\n {e}')
    else:
        t_base = n_base * float(amount)
        text = f'цена {amount} {quote} в {base} - {t_base}'
        bot.send_message(massege.chat.id, text)


bot.polling()
