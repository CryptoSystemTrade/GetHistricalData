import datetime
import json
import os
from typing import Dict, Union

import const
import pandas as pd
import requests
import util


def get_ls_rate() -> None:
    """
    LS比率をcoinglassから取得してHDF形式で保存
    """
    url = const.BASE_URI + "longShort_chart"
    currencys = [
        "BTC",
        "ETH",
    ]

    for currency in currencys:
        params: Dict[str, Union[int, str]] = {"interval": 2, "symbol": currency}
        res = requests.get(url, headers=const.HEADERS, params=params)

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
            df,dt = util.filter_df(df,span="day")

            # パスを指定
            dir_path = f"histrical-data/ls/{dt.year}/{dt.month}"
            file_name = f"{dt.year}_{dt.month}_{dt.day}_{currency}.h5"
            util.save_as_hdf(df,file_name,dir_path)


if __name__ == "__main__":
    get_ls_rate()
