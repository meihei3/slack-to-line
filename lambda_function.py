# -*- coding: utf-8 -*-
import os
import sys
import logging
import json
import re

sys.path.append('./packages/')
import requests

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

rep_ptn = re.compile("\<\@[A-Z0-9]+\>\s")

def lambda_handler(event, context):

    # 受信データをCloud Watchログに出力
    logging.info(json.dumps(event))

    # SlackのEvent APIの認証
    if "challenge" in event:
        return event["challenge"]

    # tokenのチェック
    if not is_verify_token(event):
        return "OK-verify"

        # ボットへのメンションでない場合
    if not is_app_mention(event):
        return "OK-mention"

    # Slackにメッセージを投稿する
    message = replace_message(event.get("event").get("text"))
    post_message_to_channel(event.get("event").get("channel"), message)
    post_message_to_line(message)

    return 'OK-all'


def post_message_to_channel(channel: str, message: str):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer {0}".format(os.environ["SLACK_BOT_USER_ACCESS_TOKEN"])
    }
    payload = {
        "token": os.environ["SLACK_BOT_VERIFY_TOKEN"],
        "channel": channel,
        "text": "lineにメッセージを送信しました。\n>"+message.replace("\n", "\n>"),
    }

    requests.post(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
    # urllib.request.urlopen(req)

def is_verify_token(event) -> bool:

    # トークンをチェック
    token = event.get("token")
    if token != os.environ["SLACK_BOT_VERIFY_TOKEN"]:
        return False

    return True


def is_app_mention(event):
    return event.get("event").get("type") == "app_mention"


def post_message_to_line(message: str):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer {0}".format(os.environ["LINE_TOKEN"])
    }
    payload = {
        "message": "\n"+message
    }
    requests.post(url ,headers = headers ,params=payload)


def replace_message(text: str, rep:str="") -> str:
    return rep_ptn.sub(rep, text)

