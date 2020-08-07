import logging
import requests
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from data import *

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level = logging.INFO)
logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text('Hi! Type the URL you want to shorten.')

def shorten(update, context):
    headers = {
        'Authorization': f'Bearer {BITLY_API_KEY}',
        'Content-Type': 'application/json',
    }
    link = update.message.text 
    if link[0:7] != 'http://' or link[0:7] != 'https://':
        link = 'http://' + link
    try:
        link = requests.get(link)
    except requests.exceptions.ConnectionError:
        update.message.reply_text('Website not found! Enter another URL.')
    else:
        link = link.url
        data = {
            'long_url': f'{link}'
        } 
        data = json.dumps(data)
        response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers = headers, data = data)
        json_data = json.loads(response.text)
        update.message.reply_text(json_data['id'])

def main():
    # creating the Updater and passing bot's token
    updater = Updater(f'{TELEGRAM_BOT_API_KEY}', use_context = True)
    
    # registering handlers
    dp = updater.dispatcher

    # commands and answers in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, shorten))

    # start the bot 
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, 
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()