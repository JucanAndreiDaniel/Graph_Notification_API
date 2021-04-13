import time
import sys
from pycoingecko import CoinGeckoAPI
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')
django.setup()

from registration.models import crypto_id

cg = CoinGeckoAPI()

currencies = ["usd", "eur", "gbp", "rub"]


def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)

    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" %
                   (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()


def correcttime(timestamp: str):
    try:
        timestamplist = timestamp.split("T")
        correct = timestamplist[0]+" "+timestamplist[1][:-1]
    except:
        correct="2000-01-01 00:00:00"
        print(f"{timestamp}\n")
    return correct


for i in progressbar(range(1, 26)):
    price_list = []
    for curr in currencies:
        price = cg.get_coins_markets(
            vs_currency=curr, per_page="250", page=f"{i}")
        price_list += price
    for j in range(250):
        new_coin = crypto_id(id=price_list[j]["id"], symbol=price_list[j]["symbol"],
                            name=price_list[j]["name"], image=price_list[j]["image"], high_1d_usd=price_list[j]["high_24h"],
                            high_1d_euro=price_list[j+250]["high_24h"], high_1d_gbp=price_list[j+500]["high_24h"],
                            high_1d_rub=price_list[j+750]["high_24h"], low_1d_usd=price_list[j]["low_24h"],
                            low_1d_euro=price_list[j+250]["low_24h"], low_1d_gbp=price_list[j+500]["low_24h"],
                            low_1d_rub=price_list[j+750]["low_24h"], curr_usd=price_list[j]["current_price"],
                            curr_euro=price_list[j+250]["current_price"], curr_gbp=price_list[j+500]["current_price"],
                            curr_rub=price_list[j+750]["current_price"], ath_usd=price_list[j]["ath"],
                            ath_euro=price_list[j+250]["ath"], ath_gbp=price_list[j+500]["ath"],
                            ath_rub=price_list[j+750]["ath"], atl_usd=price_list[j]["atl"],
                            atl_euro=price_list[j+250]["atl"], atl_gbp=price_list[j+500]["atl"],
                            atl_rub=price_list[j+750]["atl"], ath_time=correcttime(
                                price_list[j]["ath_date"]),
                            atl_time=correcttime(price_list[j]["atl_date"]), last_updated=correcttime(price_list[j]["last_updated"]))
        new_coin.save()
