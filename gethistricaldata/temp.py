import gzip
import os
import pathlib
from datetime import date, timedelta
from pathlib import Path

import requests
from util import hdf_into_space

url = "https://public.bybit.com/spot_index/BTCUSD/"
ds = date(2022, 1, 1)
de = date(2022, 6, 14)


def get_price_data() -> None:
    for i in range((de - ds).days + 1):
        date = ds + timedelta(i)
        day_str = str(date.day).zfill(2)
        month_str = str(date.month).zfill(2)
        file_name = f"BTCUSD2022-{month_str}-{day_str}_index_price.csv.gz"
        urlData = requests.get(url + file_name).content
        save_path = f"histrical-data/price/bybit/2022/{date.month}/2022_{date.month}_{date.day}_BTC.gz"
        with open(save_path, mode="wb") as f:  # wb でバイト型を書き込める
            f.write(urlData)

    for file_path in pathlib.Path("./histrical-data/price/bybit/2022").rglob("*"):
        if Path.is_file(file_path):
            if ".gz" in str(file_path):
                with gzip.open(file_path, mode="rb") as gzip_file:
                    content = gzip_file.read()
                    target_path = str(file_path).replace(".gz", ".csv")
                    with open(target_path, mode="wb") as decompressed_file:
                        decompressed_file.write(content)
                        os.remove(str(file_path))

    hdf_into_space()


if __name__ == "__main__":
    get_price_data()
