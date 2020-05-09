from io import BytesIO
from os import environ

from PIL import Image
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ImageMessage, ImageSendMessage)

from watermarker import watermark_with_transparency

app = Flask(__name__)

CHAN_ACCESS_TOKEN = environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
CHAN_SECRET = environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(CHAN_ACCESS_TOKEN)
handler = WebhookHandler(CHAN_SECRET)


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


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    msg = event.message
    img_id = msg.id
    print(f"Image retrieved: {img_id}")
    content = line_bot_api.get_message_content(img_id)
    img = Image.open(BytesIO(content.content))
    watermark_with_transparency(img, img_id)
    link = f"https://watermarker-th447rajwq-de.a.run.app/static/{img_id}.png"
    thumbnail = f"https://watermarker-th447rajwq-de.a.run.app/static/{img_id}-thumbnail.png"
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(original_content_url=link, preview_image_url=thumbnail)
    )


if __name__ == "__main__":
    app.run(port=environ.get("PORT", 5000))
