import datetime
import logging
import os
import pathlib
import traceback
from pathlib import Path
from typing import Tuple

import boto3
import const
import pandas as pd
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def hdf_into_space() -> None:
    """
    dataフォルダ内にあるh5形式のファイルをすべてspaceに保存してdataからは削除
    """
    session = boto3.session.Session()
    client = session.client(
        "s3",
        region_name="sgp1",
        endpoint_url="https://sgp1.digitaloceanspaces.com/",
        aws_access_key_id=const.SPACE_KEY,
        aws_secret_access_key=const.SPACE_SECRET,
    )
    space_name = "boolion"
    for file_path in pathlib.Path("./histrical-data").rglob("*"):
        if Path.is_file(file_path):
            client.upload_file(str(file_path), space_name, str(file_path))
            os.remove(str(file_path))


def filter_df(df: pd.DataFrame, span: str = "day") -> Tuple[pd.DataFrame, datetime.datetime]:
    # 現在の日本時刻
    dt_now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    dt = dt_now
    # 指定した基準日ごとに揃える
    if span == "day":
        delta = relativedelta(days=1)
        dt = dt_now - delta
        year = dt.year
        month = dt.month
        day = dt.day
    elif span == "month":
        delta = relativedelta(months=1)
        dt = dt_now - delta
        year = dt.year
        month = dt.month
        day = 1
    elif span == "year":
        delta = relativedelta(year=1)
        dt = dt_now - delta
        year = dt.year
        month = 1
        day = 1

    # 日付切り替え時刻+9時間のtimestampになるので修正
    s_timestamp = pd.Timestamp(year, month, day) + datetime.timedelta(hours=-9)
    e_timestamp = pd.Timestamp(year, month, day) + datetime.timedelta(hours=-9) + delta
    df = df[(df["timestamp"] >= s_timestamp.timestamp()) & (df["timestamp"] < e_timestamp.timestamp())]
    return df, dt


def save_as_hdf(df: pd.DataFrame, file_name: str, dir_path: str) -> None:
    os.makedirs(dir_path, exist_ok=True)
    h5 = pd.HDFStore(dir_path + "/" + file_name, "w")
    h5["data"] = df
    h5.close()


def error_handle() -> None:
    error_txt = traceback.format_exc()
    logger.error(error_txt)
