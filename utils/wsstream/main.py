#!/usr/bin/env python3

# NEEDED DOCS:
#   https://websockets.readthedocs.io/en/10.4/
#   https://dydxprotocol.github.io/v3-teacher/#v3-websocket-api

import asyncio
import websockets
import logging
import json
import urllib
import base64
import argparse
import os

DYDX_URI="wss://api.dydx.exchange/v3/ws"

class dydx:
    def __init__(self, uri):
        self.uri = uri
        self.ws = websockets.connect(uri)

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}), {!r})'.format(class_name, *self)

    # TODO: Move connecting to the websocket its own method and simplify read_ws
    async def connect(self):
        try:
            async with websockets.connect(uri) as websocket:
                self.open = websocket
        except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed, websockets.InvalidState, websockets.PayloadTooBig, websockets.ProtocolError) as e:
                print(e)

    async def read_ws(self):
        while True:
            try:
                msg = await self.open.recv()
            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed, websockets.InvalidState, websockets.PayloadTooBig, websockets.ProtocolError) as e:
                print(e)
                self.open = await websockets.connect(self.uri)  # reconnect to websocket
                msg = await self.open.send(self.subscription)
                continue
            except Exception as e:
                print(e)
                quit()
            else:
                print("received on read {}", msg)

    async def write_ws(self, payload):
        retry = 0
        connected = False
        self.subscription = payload
        while retry < 3:
            print("send attempt {}", retry)
            try:
                match connected:
                    case True:
                        print("connected")
                        break
                    case False:
                        async with self.ws as websocket:
                            self.open = websocket
                            msg = await websocket.send(payload)
                            connected = True
            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed, websockets.InvalidState, websockets.PayloadTooBig, websockets.ProtocolError) as e:
                quit()
            except Exception as e:
                print(e)
            else:
                print("received from write: {}", msg)
                if msg == None:
                    print("failed to subscribe")
                    retry +=1
                    continue
        if retry == 3 and connected == False:
            quit()


# https://docs.dydx.exchange/?json#initial-response-2
def orderbookreq(asset, offset):
    req = {
        "type": "subscribe",
        "channel": "v3_orderbook",
        "id": asset,
        "includeOffsets": offset,
    }
    print("sending orderbook subscription", req)
    return json.dumps(req).encode()

def marketsupdatereq(asset):
    req = {
        "type": "subscribe",
        "channel": "v3_markets",
    }
    print("sending marketsupdatereq subscription", req)
    return json.dumps(req).encode()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', type=str, default='')
    parser.add_argument('--stream', type=str, default='')
    args = parser.parse_args()
    if args.asset == '' and args.stream == '':
        print("must define --asset to stream")
        print("must define --stream as orderbooks or marketsupdate")
        quit()
    asset = args.asset
    exchange = dydx(DYDX_URI)
    match args.stream:
        case "orderbooks":
            await exchange.write_ws(orderbookreq(asset, "false"))
        case "marketsupdatereq":
            await exchange.write_ws(marketsupdatereq(asset))
        case _:
            print("stream must be defined as orderbooks or marketsupdatereq")
            quit()
    # while True:
    await exchange.read_ws()

if __name__ == "__main__":
    print("running stream")
    asyncio.run(main())
