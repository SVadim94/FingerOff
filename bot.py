import traceback

import telebot

import config
from handlers import handlers

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def calculator(message):
    try:
        cmd = message.text.split(' ')
        msg = handlers.get(cmd[0], handlers['/usage'])(message, *cmd[1:])
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.send_message(message.chat.id, "An error occured (see /usage)")
        traceback.print_exc()

if __name__ == '__main__':
    bot.polling(none_stop=True)
