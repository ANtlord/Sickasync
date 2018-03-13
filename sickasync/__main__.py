import time
import asyncio
import uvloop
from aiohttp import web
import aiohttp
import os

HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8080))

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


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


def main():
    app = web.Application()
    app.router.add_get('/', handle)
    app.router.add_route('GET', '/ws', websocket_handler)
    web.run_app(app, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
