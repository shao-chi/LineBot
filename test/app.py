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

app = Flask(__name__)

line_bot_api = LineBotApi('e5RbB7SpFc+2lVvFgNvSrrqdP0ewqgdfKgKjtKekO2PLRGJ5gXWbW8GgjsZmNxHRFIYhCSAuYfjzd9d7F2slB9pyBeu//819d9hJsTFRVhPmB2O23OIhw4JVYmYIxGjppHiivxJvvSIkwRe5UF0xpAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d161e3a1699942a435d11ebf0ad04253')


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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()