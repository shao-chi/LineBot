#app.py
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

from linebot_function import en_dictionary

app = Flask(__name__)

line_bot_api = \
    LineBotApi('yizrFotfzhHrVUSlSC98/TBnMfiJRzXyZ43XWNYGgG+2JrXq8EZ+RsUoSc2Egpik \
        /soa9dcfd5WgsiwuhQrGGzYqG5U1Mh8jarNP6/kCk93/NHBl2X2lkj3xx2ODKQ62r+TfiMU6 \
        xG2BqKdPWRUPOwdB04t89/1O/w1cDnyilFU=')
handler = \
    WebhookHandler('65050cc53fbb7ded70a1213824ae8894')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    word = event.message.text
    result = en_dictionary(word)

    for res in result:
        text = word + ' ({})'.format(res['part_of_speech'])
        line_bot_api.reply_message(
            event.reply_token, [ \
                TextSendMessage(text=text), \
                TextSendMessage(text='UK pronounciation'), \
                AudioSendMessage(original_content_url=res['uk_kk']), \
                TextSendMessage(text='US pronounciation'), \
                AudioSendMessage(original_content_url=res['us_kk'])])

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)