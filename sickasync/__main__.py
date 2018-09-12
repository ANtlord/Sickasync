import time
import asyncio
#  import uvloop
from aiohttp import web
import aiohttp
import os
import sys
import json

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

#  asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def scheduled_message(ws):
    await ws.send_str('Subscribed')
    for _ in range(5):
        await asyncio.sleep(1)
        await ws.send_str('Send arbitrary message')


async def websocket_handler(request: aiohttp.web_request.Request):
    print(type(request.app))
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    while True:
        await ws.send_str('["Send_flood"]')
        print(123)
        await asyncio.sleep(0.05)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            elif msg.data == 'subscribe':
                await scheduled_message(ws)
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


def server_main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_route('GET', '/ws', websocket_handler)
    web.run_app(app, host=HOST, port=PORT)


#  HOST = os.getenv('HOST', '0.0.0.0')
#  PORT = int(os.getenv('PORT', 8080))

#  URL = 'wss://api.bitfinex.com/ws/2'

import time

async def client():
    last_time = time.time()
    isSubscribed = False
    session = aiohttp.ClientSession()
    async with session.ws_connect(HOST) as ws:
        async for msg in ws:
            if not isSubscribed:
                #  if msg.type in (aiohttp.WSMsgType.OPENED,):
                await ws.send_str(json.dumps({
                  "event": "subscribe",
                  "channel": "book",
                  "symbol": "tBTCUSD",
                  "prec": "P0",
                  "freq": "F1",
                  "len": 1
                }))
                isSubscribed = True
            else:
                new_time = time.time()
                print(new_time - last_time)
                last_time = new_time
                #  print(msg.data)
            if msg.type in (aiohttp.WSMsgType.CLOSED,
                            aiohttp.WSMsgType.ERROR):
                break


def client_main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client())


def main():
    mode = sys.argv[1]
    if mode == 'ws_client':
        client_main()
    elif mode == 'http_server':
        server_main()


if __name__ == "__main__":
    main()
