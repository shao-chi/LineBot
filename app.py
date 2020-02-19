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
import config

app = Flask(__name__)

line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)


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

    # line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text=text))

    for res in result:
        text = word + ' ({})'.format(res['part_of_speech'])
        line_bot_api.push_message(
            config.USER_ID, TextSendMessage(text=text))
        line_bot_api.push_message(
            config.USER_ID, TextSendMessage(text='UK pronounciation'))
        line_bot_api.push_message(
            config.USER_ID, TextSendMessage(text='UK pronounciation'))
        line_bot_api.push_message(
            config.USER_ID, \
            AudioSendMessage(original_content_url=res['uk_audio'], duration=240000))
        line_bot_api.push_message(
            config.USER_ID, TextSendMessage(text='US pronounciation'))
        line_bot_api.push_message(
            config.USER_ID, \
            AudioSendMessage(original_content_url=res['us_audio'], duration=240000))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)