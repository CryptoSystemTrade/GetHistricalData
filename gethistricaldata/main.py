import datetime
import json
import os
from os.path import dirname, join
from pathlib import Path
from typing import Dict, Union

import boto3
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)


COINGLASS_TOKEN = os.environ.get("COINGLASS_TOKEN")
SPACE_SECRET = os.environ.get("SPACE_SECRET")
SPACE_KEY = os.environ.get("SPACE_KEY")


base_uri = "http://open-api.coinglass.com/api/pro/v1/futures/"
headers = {"coinglassSecret": COINGLASS_TOKEN}


def main() -> None:
    """
    coingrass.comから各種ヒストリカルデータを取得する関数

    """
    print("start get data")

    print("get L/S chart")
    # get_ls_rate()

    print("save hdf5 into spaces")
    # 取得したh5ファイルをすべてSpaceに保存し、ローカルからは削除
    hdf_into_space()


def get_ls_rate() -> None:
    """
    LS比率をcoinglassから取得してHDF形式で保存
    """
    url = base_uri + "longShort_chart"
    currencys = [
        "BTC",
        "ETH",
    ]

    for currency in currencys:
        params: Dict[str, Union[int, str]] = {"interval": 2, "symbol": currency}
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
            df = df[(df["timestamp"] >= s_timestamp.timestamp()) & (df["timestamp"] < e_timestamp.timestamp())]

            # パスを指定
            dir_path = f"histrical-data/ls/{year}/{month}"
            file_name = f"{year}_{month}_{day}_{currency}.h5"
            os.makedirs(dir_path, exist_ok=True)
            h5 = pd.HDFStore(dir_path + "/" + file_name, "w")
            h5["data"] = df
            h5.close()


def hdf_into_space() -> None:
    """
    dataフォルダ内にあるh5形式のファイルをすべてspaceに保存してdataからは削除
    """
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="sgp1",
        endpoint_url="https://sgp1.digitaloceanspaces.com/",
        aws_access_key_id=SPACE_KEY,
        aws_secret_access_key=SPACE_SECRET,
    )
    space_name = "boolion"
    for file_path in Path("./histrical-data").rglob("*"):
        if Path.is_file(file_path):
            client.upload_file(str(file_path), space_name, str(file_path))
            os.remove(str(file_path))


if __name__ == "__main__":
    main()
