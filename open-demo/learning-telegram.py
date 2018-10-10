import logging
from telegram.ext import Updater, CommandHandler

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def get(bot, update):
	bot.send_photo(chat_id=chat_id, photo=open('test.jpg', 'rb'))



updater = Updater(token="629389428:AAGeiLSafnaVEwTfqA67TNpNcucnPsE2HTo")
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
start_handler = CommandHandler('get', get)
dispatcher.add_handler(start_handler)

updater.start_polling()


