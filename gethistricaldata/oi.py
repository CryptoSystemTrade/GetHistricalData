import json
from typing import Dict, List, Union

import const
import pandas as pd
import requests
import util


def get_oi_rate() -> None:
    """
    FR比率をcoinglassから取得してHDF形式で保存
    1ヶ月ごとの実行
    """
    url = const.BASE_URI + "openInterest/chart"
    currencys = [
        "BTC",
        "ETH",
    ]

    for currency in currencys:
        params: Dict[str, Union[str, int]] = {"interval": 2, "symbol": currency}
        res = requests.get(url, headers=const.HEADERS, params=params)

        res_json = json.loads(res.text)
        if "data" in res_json:
            data = res_json["data"]

            prices = data["priceList"]
            date_list = data["dateList"]

            df = pd.DataFrame(
                list(zip(prices, date_list)),
                columns=["price", "timestamp"],
            )
            df["timestamp"] = df["timestamp"] / 1000

            data_map: Dict[str, List[int]] = data["dataMap"]
            for site in data_map.keys():
                df[site] = data_map[site]

            df, dt = util.filter_df(df, span="day")

            # パスを指定
            dir_path = f"histrical-data/oi/{dt.year}/{dt.month}"
            file_name = f"{dt.year}_{dt.month}_{dt.day}_{currency}.h5"
            util.save_as_hdf(df, file_name, dir_path)


if __name__ == "__main__":
    get_oi_rate()
