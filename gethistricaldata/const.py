import os
from os.path import dirname, join

from dotenv import load_dotenv

load_dotenv(verbose=True)
env_path = join(dirname(__file__), ".env")
load_dotenv(env_path)


COINGLASS_TOKEN = os.environ.get("COINGLASS_TOKEN")
SPACE_SECRET = os.environ.get("SPACE_SECRET")
SPACE_KEY = os.environ.get("SPACE_KEY")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")


BASE_URI = "http://open-api.coinglass.com/api/pro/v1/futures/"
HEADERS = {"coinglassSecret": COINGLASS_TOKEN}
