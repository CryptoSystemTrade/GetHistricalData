import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import pandas as pd
import datetime
import time

load_dotenv(verbose=True)
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)


COINGLASS_TOKEN = os.environ.get("COINGLASS_TOKEN")
base_uri = "http://open-api.coinglass.com/api/pro/v1/futures/"
headers = {"coinglassSecret": COINGLASS_TOKEN}


def main():
    """
    coingrass.comから各種ヒストリカルデータを取得する関数

    """
    print("start get data")

    print("get L/S chart")


def get_ls_rate():
    url = base_uri + "longShort_chart"
    currencys = [
        "BTC",
        "ETH",
    ]

    for currency in currencys:
        params = {"interval": 2, "symbol": currency}
        res = requests.get(url, headers=headers, params=params)

        res_json = json.loads(res.text)
        if "data" in res_json:
            data = res_json["data"]
            l_rates = data["longRateList"]
            s_rates = data["shortsRateList"]
            prices = data["priceList"]
            ls_rates = data["longShortRateList"]
            date_list = data["dateList"]

            df = pd.DataFrame(
                list(zip(prices, ls_rates, l_rates, s_rates, date_list)),
                columns=["price", "LS_Rate", "L_Rate", "S_Rate", "timestamp"],
            )
            df["timestamp"] = df["timestamp"] / 1000

            # プログラム実行の前日のデータのみ取得
            # 現在の日本時刻
            dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))) + datetime.timedelta(days=-1)
            year = dt_now.year
            month = dt_now.month
            day = dt_now.day

            # 日付切り替え時刻+9時間のtimestampになるので修正
            s_timestamp = pd.Timestamp(year, month, day) + datetime.timedelta(hours=-9)
            e_timestamp = pd.Timestamp(year, month, day) + datetime.timedelta(hours=-9) + datetime.timedelta(days=1)
            df = df[(df['timestamp'] >= s_timestamp.timestamp()) &  (df["timestamp"] < e_timestamp.timestamp())]

            h5 = pd.HDFStore(f"data/{year}_{month}_{day}.h5","w")
            h5["data"] = df
            h5.close()



if __name__ == "__main__":
    main()
