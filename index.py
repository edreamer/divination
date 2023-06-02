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

import random
import requests
from bs4 import BeautifulSoup
import pandas as pd
def gua(q):
   gua_dict = {1: "乾", 2: "坤", 3: "屯", 4: "蒙", 5: "需", 6: "訟", 7: "師", 8: "比", 9: "小畜", 10: "履", 11: "泰", 12: "否", 13: "同人", 14: "大有", 15: "謙", 16: "豫", 17: "隨", 18: "蠱", 19: "臨", 20: "觀", 21: "噬嗑", 22: "贅", 23: "訟", 24: "復", 25: "無妄", 26: "大畜", 27: "頤", 28: "大過", 29: "坎", 30: "離", 31: "鹹", 32: "恆", 33: "遯", 34: "大壯", 35: "晉", 36: "明夷", 37: "家人", 38: "睽", 39: "蹇", 40: "解", 41: "損", 42: "益", 43: "夬", 44: "姤", 45: "萃", 46: "升", 47: "困", 48: "井", 49: "革", 50: "鼎", 51: "震", 52: "艮", 53: "漸", 54: "歸妹", 55: "豐", 56: "旅", 57: "巽", 58: "兌", 59: "渙", 60: "節", 61: "中孚", 62: "小過", 63: "既濟", 64: "未濟"}
   zhi_dict = {1: "初爻", 2: "二爻", 3: "三爻", 4: "四爻", 5: "五爻", 6: "上爻"}
   result_dict = {"陽爻": " ——————○——————", "陰爻": " —————   ————— "}
   yao_list = [random.randint(0, 1) for i in range(6)]
   result_list = [result_dict["陰爻"] if yao == 1 else result_dict["陽爻"] for yao in yao_list]
   gua_num = sum([yao_list[i] * 2**(5-i) for i in range(6)]) + 1
   for i in range(6):
       msg=zhi_dict[i+1]+result_list[i]+"\n"
   msg+=gua_dict[gua_num]+"\n"

   url = "https://www.newton.com.tw/wiki/%E6%98%93%E7%B6%93%E5%85%AD%E5%8D%81%E5%9B%9B%E5%8D%A6"
   response = requests.get(url)
   soup = BeautifulSoup(response.text, 'html.parser')
   msg1=soup.find('div',id="body").find('article').find('div',id='content')
   msg2=msg1.find_all('div',class_="wiki")
   i=gua_num*3
   msg3=msg2[i].text
   msg+=msg3.replace("。","。\n")
   url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQYAah11varWLxPaoQNoeG2oaReLqfe_W0GMAq9kFbfl0sdhtxIimTymFvoF2JSw-PZDtt3xWx3eSV1/pub?gid=2034558057&single=true&output=csv'
   df = pd.read_csv(url)
   df1=df[df['卦象']==gua_num]
   msg+=df1['問事']+":"+df1['解釋']
   return msg

app = Flask(__name__)

line_bot_api = LineBotApi('oGueiClujjHgpB7H4ukWLGy2tby8w4j+bJwNxKDW6XrIUQUch7y4QZNep49ozPNpdfN/gScOu81eHqaRk1TLC5zQxMDGKmRD9/HpP0ST9dfSm6/xHJpCjbZuk6/BuEKCaxozOiYXX92wdIBT+VQkNwdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('c2ae5e0dc30dd3efc87128e58e197e4a c2ae5e0dc30dd3efc87128e58e197e4a')


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
        abort(400)

    return 'OK'


@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=gua(event.message.text)))


if __name__ == "__main__":
    app.run()
