from datetime import date

from utalib.client import get_price_data_binance

get_price_data_binance(
    currency="BTCUSDT", product="spot", category="klines", minute=15, s_date=date(2021, 11, 1), e_date=date(2022, 6, 1)
)
