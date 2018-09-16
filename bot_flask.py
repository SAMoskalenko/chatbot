from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests
import json
import re


app = Flask(__name__)
sslify = SSLify(app)


TOKEN = '677329060:AAEmvnJgXsQisyJ4ER7Imosjam0_Xu1lyys'
URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


def write_json(data, filename='answer.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def send_message(chat_id, text='bla, bla, bla'):
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(URL + 'sendMessage', json=answer)
    return r.json()


def parse_text(text):
    pattern = r'/\w+'
    crypto = re.search(pattern, text).group()
    return crypto[1:]


def get_price(crypto):
    url = 'https://api.coinmarketcap.com/v1/ticker/{}'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        pattern = r'/\w+'

        if re.search(pattern, message):
            price = get_price(parse_text(message))
            send_message(chat_id, text=price)

        # write_json(r)
        return jsonify(r)
    return '<h1>Empire Welcomes You</h1>'


if __name__ == '__main__':
    app.run()