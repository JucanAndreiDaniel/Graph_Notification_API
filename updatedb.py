import traceback
import sys
from pycoingecko import CoinGeckoAPI
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')
django.setup()


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
        correct = timestamplist[0]+" "+timestamplist[1][:-1]+"+00:00"
    except:
        correct = "2000-01-01 00:00:00+00:00"
        print(f"{timestamp}\n")
    return correct


try:
    import registration.models as mod
    for i in progressbar(range(1, 26)):
        price_list = []
        for curr in currencies:
            price = cg.get_coins_markets(
                vs_currency=curr, per_page="250", page=f"{i}")
            price_list += price
        for j in range(250):
            coin = mod.crypto_id(id=price_list[j]["id"], symbol=price_list[j]["symbol"],
                                 name=price_list[j]["name"], image=price_list[j]["image"], last_updated=correcttime(
                price_list[j]["last_updated"]))
            coin.save()
            for k in range(4):
                value = mod.value(coin_currency=f"{price_list[j]['id']}_{currencies[k]}", coin_id=coin,
                                  currency=currencies[k], current=price_list[j +
                                                                             (250*k)]["current_price"],
                                  high_1d=price_list[j+(250*k)]["high_24h"], low_1d=price_list[j+(
                                      250*k)]["low_24h"],
                                  ath=price_list[j+(250*k)]["ath"], ath_time=correcttime(
                                      price_list[j+(250*k)]["ath_date"]),
                                  atl=price_list[j+(250*k)]["ath"], atl_time=correcttime(price_list[j+(250*k)]["atl_date"]))
                value.save()


except:
    traceback.print_exc()
