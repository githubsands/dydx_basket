import os
import time
import seaborn as sns

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from datetime import datetime
from pycoingecko import CoinGeckoAPI

class asset:
    def __init__(self, name, twitter):
        self.name = name
        self.tweets = twitter

assets = {
    "ETH": 'ethereum',
    "BTC": 'bitcoin',
    "MATIC": 'matic-network',
    "SOL": 'solana',
    "ADA": 'cardano',
    "YFI": 'yearn-finance',
    "SUSHI": 'sushi',
    "NEAR": 'near',
    "DOGE": 'dogecoin',
    "AVAX": 'avalanche-2',
    "LTC": 'litecoin',
    "LINK": 'chainlink',
    "ALGO": 'algorand',
    "CRV": 'curve-dao-token',
    "MKR": 'maker',
    "DOT": 'polkadot',
    "ZEC": 'zcash',
    "ETC": 'ethereum-classic',
    "BCH": 'bitcoin-cash',
    "ZRX": '0x',
    "TRX": 'tron',
    "SNX": 'havven',
    "AAVE": 'aave',
    "ATOM": 'cosmos',
    "UNI": 'uniswap',
    "XTZ": 'tezos',
    "ICP": 'internet-computer',
    "FIL": 'filecoin',
    "COMP": 'compound-governance-token',
    "RUNE": 'thorchain',
    "EOS": 'eos',
    "XMR": 'monero',
    "1INCH": '1inch',
    "CELO": 'celo',
    "ENJ": 'enjincoin',
    "XLM": 'stellar',
    "UMA": 'uma',
}

def save_historical_prices(cg_client):
    data = []
    for key in assets:
        try:
            print("receiving historical data for ", key)
            df = cg_client.get_coin_market_chart_range_by_id(id=assets[key],vs_currency='usd',from_timestamp='1605099700',to_timestamp='1605099600')
            data.append(df)
        except ValueError as e:
            print("failed to get currency {}, error received e", key, e)
            continue
    try:
        np.savetxt("data/historical-prices.csv", data, fmt='%s', delimiter="")
    except ValueError as e:
        print("failed to get currency {}, error received e", key, e)

def get_single_asset_price_and_volume(cg_client, asset):
    current_time = str(time.time())
    data = []
    try:
        print("receiving historical data for bitcoin")
        data = cg_client.get_coin_market_chart_range_by_id(id=asset,vs_currency='usd',from_timestamp='0',to_timestamp=current_time,xlabel='timestamp',ylabel='volume',title='dydx basket total volumes')
        df_price=pd.DataFrame(data["prices"], columns=['time','price'])
        df_volume=pd.DataFrame(data["total_volumes"], columns=['time','volume'])
    except Exception as e:
        print("failed to received the data: ", e)
    else:
        pd.DataFrame(df_price).to_csv("data/historical-prices.csv")
        pd.DataFrame(df_volume).to_csv("data/historical-volumes.csv")
        plt.plot(df_price.time, df_price.price)
        plt.show()
        plt.plot(df_price.time, df_volume.volume)
        plt.show()

def plot_all_asset_volumes_single_graph(cg_client):
    current_time = str(time.time())
    data = []
    for key in assets:
        try:
            data = cg_client.get_coin_market_chart_range_by_id(id=assets[key],vs_currency='usd',from_timestamp='0',to_timestamp=current_time)
            df_volume=pd.DataFrame(data["total_volumes"], columns=['time','total_volumes'])
            plt.plot(df_volume.time, df_volume.total_volumes, label=key)
        except Exception as e:
            print("failed to received the data: ", e)

    plt.title('dydx basket historic volumes')
    plt.xlabel('timestamp')
    plt.ylabel('volumes')
    plt.legend()
    plt.show()

def plot_all_asset_volumes(cg_client):
    current_time = str(time.time())
    data = []
    print("making grid:", round(len(assets)/3)+1,3)
    fig, axs = plt.subplots(nrows=round(len(assets)/3)+1,ncols=3)
    fig.suptitle('dydx basket change in volumes')
    subplot_x = 0
    subplot_y = 0
    asset_num = 1
    for key in assets:
        # TODO: Fix this bug
        if key == "MKR":
            break
        try:
            print(asset_num, "receiving historical data for", key, "grid", subplot_x, subplot_y)
            data = cg_client.get_coin_market_chart_range_by_id(id=assets[key],vs_currency='usd',from_timestamp='0',to_timestamp=current_time)
            #x=pd.DataFrame(data["prices"], columns=['time','prices'])
            xy=pd.DataFrame(data["total_volumes"], columns=['time','total_volumes'])
        except Exception as e:
            print("failed to received the data: ", e)
        else:
            if subplot_x > 3:
                subplot_x=0
                subplot_y+=1
            else:
                subplot_x+=1
            axs[subplot_x,subplot_y].plot(xy.time, xy.total_volumes)
            asset_num+=1
    plt.show()

# def correlate

def graph_historical_volumes_btc(cg_client):
    data = []
    try:
        print("receiving historical data for bitcoin")
        df = cg_client.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp='0',to_timestamp='1605099600')
        volumes=df["total_volumes"]
        data.append(volumes)
        array = np.array(volumes)
        df.head()
    except ValueError as e:
        print("failed to get currency {}, error received e", key, e)
    else:
        array = np.array(volumes)
        plt.plot(array)
        plt.show()

def graph_historical_prices_btc(cg_client):
    data = []
    try:
        print("receiving historical data for bitcoin")
        df = cg_client.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp='0',to_timestamp='1605099600')
        prices=df["prices"]
    except ValueError as e:
        print("failed to get currency {}, error received e", key, e)
    else:
        array = np.array(volumes)
        plt.plot(array)
        plt.show()

def get_historical_prices(cg_client):
    data = []
    for key in assets:
        try:
            print("receiving historical data for ", key)
            df = cg_client.get_coin_market_chart_range_by_id(id=assets[key],vs_currency='usd',from_timestamp='0',to_timestamp='1605099600')
            data.append(df)
        except ValueError as e:
            print("failed to get currency {}, error received e", key, e)
            continue
    return np.array(data)


def get_historical_volumes(cg_client, period, ranges):
    data = []
    for key in assets:
        try:
            print("receiving historical volume", key)
            df = cg_client.get_coin_market_chart_range_by_id(id=assets[key],vs_currency='usd',from_timestamp='0',to_timestamp='1605099600')
            volumes=df[total_volumes]
            data.append(volumes)
        except ValueError as e:
            print("failed to get currency {}, error received e", key, e)
            continue
    np.savetxt("data/historical-volumes-"+period+".csv", data, fmt='%s', delimiter="")

# TODO - Remove this.
def save_historical_volumes_btc(cg_client):
    data = []
    try:
        print("receiving historical volume", "bitcoin")
        df = cg_client.get_coin_market_chart_range_by_id(id='bitcoin',vs_currency='usd',from_timestamp='1605099500',to_timestamp='1605099600')
        # volumes=df[total_volumes]
        data.append(df)
    except ValueError as e:
        print("failed to get currency {}, error received e", key, e)
    np.savetxt("data/historical-volumes.csv", data, fmt='%s', delimiter="")


# def get_daily_volatility(data):

def get_upstream_prices(cg_client):
    for key in assets:
        try:
            print("receiving price", cg_client.get_price(ids=[assets[key]], vs_currencies=['usd']))
        except ValueError as e:
            print("failed to get currency {}, error received e", key, e)
            continue

def convert_time(timestamp):
    return datetime.fromtimestamp(timestamp/1000)

def main():
    cg = CoinGeckoAPI()
    plot_all_asset_volumes_single_graph(cg)

if __name__ == "__main__":
     main()
