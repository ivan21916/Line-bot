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

line_bot_api = LineBotApi('MSqGL2CmAG1zf35U7fsH/FtPqhozn1wf/fAHg5YosjV514DBGMRdsacZCOuMDXxJv7QmsIuwVliFm8hk+0r7N/s5ABrXVqcGMr8hYHhUEI7iUokBa3SC2+C26ZIZquk9qLTkQhJLxc1TFSMZeGhI3QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e07b4da69d9e92e1e8f960df69fb7122')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()