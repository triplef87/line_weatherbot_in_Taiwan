# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import simplejson as json
import requests
from datetime import datetime
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        user_message = event.message.text
        #judge just echo or have to reply weather
        if "天氣" not in user_message:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.message.text)
            )
            return 'just echo'
        #judge which day have to reply
        tommorow_switch = False
        if "今天" in user_message:
            weather_reply = "今天"
        elif "明天" in user_message:
            weather_reply = "明天"
            tommorow_switch = True
        else:
            weather_reply = "現在"
        #search location name
        locateIndex = user_message.find("市")
        if locateIndex < 0:
            locateIndex = user_message.find("縣")
        location = user_message[locateIndex - 2 : locateIndex + 1]
        #load weather data
        url = "http://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?locationName=" + location + "&elememtName=Wx"
        header = {"Authorization":os.getenv('API_KEY',None)}
        resource = requests.get(url,headers=header)
        data = json.loads(resource.content)
        #find response day's data if not reply error
        try:
            dataTimeSet = data['records']['location'][0]['weatherElement'][0]['time']
            for dataTime in dataTimeSet:
                nowTime = datetime.strptime(dataTime['startTime'],"%Y-%m-%d %H:%M:%S")
                if nowTime.day == datetime.now().day or tommorow_switch:
                    reply = weather_reply + location + "的天氣為" + dataTime['parameter']['paramterName']
                    break
        except:
            reply = "Oops！！ 找不到資料 請確認地點輸入無誤"
        #if reply no data set the tommorrow's reply
        try:
            reply
        except:
            reply = "已無今日資料 明天" + location + "的天氣為" + data['records']['location'][0]['weatherElement'][0]['time'][0]['parameter']['paramterName']
        #set reply to line
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply)
        )
        return 'OK'


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
