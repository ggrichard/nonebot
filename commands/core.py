import os
import requests

from command import CommandRegistry
from apiclient import client as api

__registry__ = cr = CommandRegistry()


@cr.register('echo', '重复', '跟我念')
def echo(args_text, ctx_msg):
    msg_type = ctx_msg.get('type')
    if msg_type == 'group_message':
        api.send_group_message(gnumber=ctx_msg.get('gnumber'), content=args_text)
    elif msg_type == 'message':
        api.send_message(qq=ctx_msg.get('sender_qq'), content=args_text)


@cr.register('chat', '聊天')
def chat(args_text, ctx_msg):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': os.environ.get('TURING123_API_KEY'),
        'info': args_text
    }
    if 'sender_qq' in ctx_msg:
        data['userid'] = ctx_msg.get('sender_qq')
    resp = requests.post(url, data=data)
    if resp.status_code == 200:
        json = resp.json()
        if int(json.get('code', 0)) == 100000:
            reply = json.get('text', '')
        else:
            # Is not text type
            reply = '腊鸡图灵机器人返回了一堆奇怪的东西，就不发出来了'
    else:
        reply = '腊鸡图灵机器人出问题了，先不管他，过会儿再玩他'
    echo(reply, ctx_msg)