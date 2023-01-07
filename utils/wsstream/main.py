#!/usr/bin/env python3
# https://dydxprotocol.github.io/v3-teacher/#v3-websocket-api

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

    async def read_ws(self):
        while True:
            try:
                async with self.ws as websocket:
                    msg = await websocket.recv()
            except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed, websockets.InvalidState, websockets.PayloadTooBig, websockets.ProtocolError) as e:
                print(e)
                quit()
            except Exception as e:
                print(e)
                quit()
            else:
                print("received on read {}", msg)

    async def write_ws(self, payload):
        try:
            async with self.ws as websocket:
                msg = await websocket.send(marketsupdatereq())
        except (websockets.ConnectionClosedOK, websockets.ConnectionClosedError, websockets.ConnectionClosed, websockets.InvalidState, websockets.PayloadTooBig, websockets.ProtocolError) as e:
            print(e)
            quit()
        except Exception as e:
            print(e)
        else:
            print("received on write {}", msg)


# https://docs.dydx.exchange/?json#initial-response-2
def orderbookrequest(asset):
    req = {
        "type": "subscribed",
        "channel": "v3_orderbook",
        "id": asset,
        "contents": {
            bids: {
                price: "",
                size: "",
                offset: "",
            },
            asks: {
                price: "",
                size: "",
                offset: "",
            },
        },
        "includeOffsets": "false",
    }
    return json.dumps(req)

def marketsupdatereq():
    req = {
        "type": "subscribe",
        "channel": "v3_markets",
    }
    print(req)
    return json.dumps(req).encode()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--asset', type=str, default='')
    args = parser.parse_args()
    if args.asset == '':
        print("must define --asset to stream")
        quit()
    asset = args.asset
    exchange = dydx(DYDX_URI)
    await exchange.write_ws(marketsupdatereq())
    while True:
        await exchange.read_ws()

if __name__ == "__main__":
    print("running stream")
    asyncio.run(main())
