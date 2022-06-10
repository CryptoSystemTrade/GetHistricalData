import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import pandas as pd
import datetime
import boto3

load_dotenv(verbose=True)
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)


COINGLASS_TOKEN = os.environ.get("COINGLASS_TOKEN")
SPACE_SECRET = os.environ.get("SPACE_SECRET")
SPACE_KEY = os.environ.get("SPACE_KEY")


base_uri = "http://open-api.coinglass.com/api/pro/v1/futures/"
headers = {"coinglassSecret": COINGLASS_TOKEN}


def main():
    """
    coingrass.comから各種ヒストリカルデータを取得する関数

    """
    try:
        print("start get data")

        print("get L/S chart")
        get_ls_rate()



        print("save hdf5 into spaces")
        # 取得したh5ファイルをすべてSpaceに保存し、ローカルからは削除
        hdf_into_space()
    except:
        print("error")

def get_ls_rate():
    """
    LS比率をcoinglassから取得してHDF形式で保存
    """
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
            df = df[(df["timestamp"] >= s_timestamp.timestamp()) & (df["timestamp"] < e_timestamp.timestamp())]

            h5 = pd.HDFStore(f"histrical-data/{year}_{month}_{day}.h5", "w")
            h5["data"] = df
            h5.close()


def hdf_into_space():
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
    for dir_name in os.listdir("histrical-data"):
        for file_name in os.listdir("histrical-data/" + dir_name):
            file_path =  "histrical-data/" + dir_name + "/" + file_name
            try:
                client.upload_file(file_path, space_name, file_path)

                #成功した場合はファイル削除
                os.remove(file_path)
            except:
                print("upload Error")



if __name__ == "__main__":
    main()
