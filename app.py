# KODING UNTUK FULLFILLMENT DIALOGFLOW

from flask import Flask
import os
from flask import request
from flask import make_response
import  dialogflow
import logging
import json
import random

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

app = Flask(__name__)


# all requests from dialogflow will go throught webhook function
@app.route('/webhook', methods=['POST'])
def webhook():
    # get dialogflow request
    req = request.get_json(silent=True, force=True)

    logger.info("Incoming request: %s", req)

    intent = get_intent_from_req(req)
    logger.info('Detected intent %s', intent)
    # user asks for today's special
    if intent == 'sticker':

        # pick any :)
        response = {
            "fulfillmentMessages": [
              {
                "text": {
                  "text": [
                    "olrit"
                  ]
                },
                "platform": "LINE"
              },
              {
                "payload": {
                  "line": {
                    "type": "sticker",
                    "packageId": "1",
                    "stickerId": "1"
                  }
                },
                "platform": "LINE"
              },
              {
                "text": {
                  "text": [
                    ""
                  ]
                }
              }
            ]
        }
    else:
        # something went wrong here, we got unknow intent or request without intent
        response = {
            'fulfillmentText': 'Yeah, I\'m here but still learning, please wait for part 2 of this tutorial!',
        }

    res = create_response(response)

    return res


def get_intent_from_req(req):
    """ Get intent name from dialogflow request"""
    try:
        intent_name = req['queryResult']['intent']['displayName']
    except KeyError:
        return None

    return intent_name


def create_response(response):
    """ Creates a JSON with provided response parameters """

    # convert dictionary with our response to a JSON string
    res = json.dumps(response, indent=4)

    logger.info(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# if __name__ == '__main__':
#     app.run(debug=False, port=5000, host='0.0.0.0', threaded=True)

# Koding with heroku
# # mybot/app.py
# import os
# from decouple import config
# from flask import (
#     Flask, request, abort
# )
# from linebot import (
#     LineBotApi, WebhookHandler
# )
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage,StickerMessage, StickerSendMessage
# )
# app = Flask(__name__)
# # get LINE_CHANNEL_ACCESS_TOKEN from your environment variable
# line_bot_api = LineBotApi(
#     config("LINE_CHANNEL_ACCESS_TOKEN",
#            default=os.environ.get('LINE_ACCESS_TOKEN'))
# )
# # get LINE_CHANNEL_SECRET from your environment variable
# handler = WebhookHandler(
#     config("LINE_CHANNEL_SECRET",
#            default=os.environ.get('LINE_CHANNEL_SECRET'))
# )
#
#
# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']
#
#
#     # get request body as text
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#
#
#     # handle webhook body
#     try:
#         handler.handle(body, signature)
#     except InvalidSignatureError:
#         abort(400)
#
#
#     return 'OK'
#
#
# @handler.add(MessageEvent, message=TextMessage)
# def handle_text_message(event):
#     mess = [StickerSendMessage(package_id=11538, sticker_id=51626503), StickerSendMessage(package_id=11538, sticker_id=51626507)]
#     if event.message.text == "Hello" :
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=event.message.text)
#         )
#     elif event.message.text == "Sleep" :
#         line_bot_api.reply_message(
#             event.reply_token,
#             StickerSendMessage(package_id=1, sticker_id=1)
#         )
#     elif event.message.text == "Spirit" :
#         line_bot_api.reply_message(
#             event.reply_token,
#             mess
#         )
#     else :
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text="Sorry we don't know what you mean yet :)")
#         )
# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     app.run(host='0.0.0.0', port=port)



