from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import requests

def checkword(w):
    url = 'https://www.moedict.tw/uni/' + w
    r = requests.get(url)
    datas = r.json()
    msg = '國字：' + datas['title'] + '\n'
    msg += '部首：' + datas['radical'] + '\n'
    msg += '筆劃：' + str(datas['stroke_count']) + '\n\n'
    for i in range(len(datas['heteronyms'])):
        msg += '注音：' + datas['heteronyms'][i]['bopomofo'] + '\n'
        msg += '拼音：' + datas['heteronyms'][i]['pinyin'] + '\n'    
        for j in range(len(datas['heteronyms'][i]['definitions'])):
            if 'type' in datas['heteronyms'][i]['definitions'][j]:
                msg += '[{}] {}\n'.format(
                    datas['heteronyms'][i]['definitions'][j]['type'],
                    datas['heteronyms'][i]['definitions'][j]['def'])
        msg += '\n'
    return msg

app = Flask(__name__)

line_bot_api = LineBotApi('H7uoWOzi1LGuz4c+Lr7ELNZRXC3SNmqnjROVt25OrlloV14FhiPdkLUZjXR3B5VTW6i/diGN4XeMbI+2ZtC3JH/Pspa5jmbZFmJHm+0SqqFpMZ5Eckhq2wzn4ozLuZOFGkfRiDl7fBFQVgvclBE1+wdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('423b778a6f26f0a9a5bd79ba83ec5676 423b778a6f26f0a9a5bd79ba83ec5676')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(200)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=checkword(event.message.text)))


if __name__ == "__main__":
    app.run()
