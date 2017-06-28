from handlers import cb
import telebot
import config


bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def calculator(message):
    try:
        cmd = message.text.split(' ')
        msg = cb.get(cmd[0], cb['/usage'])(message.chat.id, *cmd[1:])
        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.send_message(message.chat.id, 'Vadim zaebal! Exception: %s' % e)

if __name__ == '__main__':
    bot.polling(none_stop=True)
