import config
import getprices

import requests
import flask
import os

import telebot

app = flask.Flask(__name__)

bot = telebot.TeleBot(config.TG_TOKEN)

URL = 'https://api.telegram.org/bot' + config.TG_TOKEN + '/'

beer_list = ['branik', 'gambrinus', 'svijany']

@app.route('/' + config.TG_TOKEN, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'Test message', 200

    else:
        flask.abort(403)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    bot.remove_webhook()
    bot.set_webhook(url="https://{}.herokuapp.com/{}".format(config.APP_NAME, config.TG_TOKEN))
    return '1'



@bot.message_handler(commands=['branik', 'Branik'])
def send_price(message):
    with open('akce/branik', 'r') as f:
        prices = f.read()
    bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    f.close()


@bot.message_handler(commands=['gambrinus', 'Gambrinus'])
def send_price(message):
    with open ('akce/gambrinus', 'r') as f:
        prices = f.read()
    bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    f.close()

@bot.message_handler(commands=['svijany', 'Svijany'])
def send_price(message):
    with open ('akce/svijany', 'r') as f:
        prices = f.read()
    bot.send_message(message.chat.id, prices, parse_mode='Markdown')
    f.close()


@bot.message_handler(commands=['refresh'])
def refresh_price(message):
    for beer in beer_list:
        getprices.parse_beer(beer)
    bot.send_message(message.chat.id, 'Обновил цены', parse_mode='Markdown')


if __name__ == '__main__':
    # main()
    for beer in beer_list:
        getprices.parse_beer(beer)
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))