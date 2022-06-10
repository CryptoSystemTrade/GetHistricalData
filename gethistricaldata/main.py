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
    pass

if __name__ == "__main__":
    main()
