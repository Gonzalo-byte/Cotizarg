from email import message
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv

load_dotenv('.env')



def start(update, context):

    button1 = InlineKeyboardButton("BTC", callback_data=BTC)
    user = update.message.from_user.first_name

    update.message.reply_text(
        text='Hola! ' + user +'\n Qué cotización te gustaría ver?',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text="BTC", callback_data='BTC')],
            [InlineKeyboardButton(text="ETH", callback_data='ETH')],
            ])
        )

def BTC(update, context):
    query = update.callback_query
    query.answer()
    price = get_btc_price()
    query.edit_message_text(text="BTC : " + str(price) + " USD")

def ETH(update, context):
    query = update.callback_query
    query.answer()
    price = get_eth_price()
    query.edit_message_text(text="ETH : " + str(price) + " USD")

def get_eth_price():
    import requests
    import json
    url =os.environ.get('URL_ETH')

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

    headers = {
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.environ.get('RAPID_API_HOST')
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    price = round(float(response['data']['price']),3)
    return price

def get_btc_price():
    import requests
    import json
    url =os.environ.get('URL_BTC')

    querystring = {"referenceCurrencyUuid":"yhjMzLPhuIDl"}

    headers = {
        "X-RapidAPI-Key": os.environ.get('RAPID_API_KEY'),
        "X-RapidAPI-Host": os.environ.get('RAPID_API_HOST')
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    price = round(float(response['data']['price']),3)
    return price

if __name__ == '__main__':
    updater = Updater(token=os.environ.get('TOKEN'),  use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(pattern='BTC', callback=BTC),
            CallbackQueryHandler(pattern='ETH', callback=ETH)
            ],
        states={},
        fallbacks={}
    ))

    #para que el bot se quede escuchando a los comandos
    updater.start_polling()
    updater.idle()