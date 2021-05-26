
from pycoingecko import CoinGeckoAPI
import time
import datetime
import traceback
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')


django.setup()


cg = CoinGeckoAPI()

currencies = ["usd", "eur", "gbp", "rub"]


def correcttime(timestamp: str):
    try:
        timestamplist = timestamp.split("T")
        correct = timestamplist[0]+" "+timestamplist[1][:-2]+"+00:00"
    except:
        correct = "2000-01-01 00:00:00+00:00"
        print(f"{timestamp}\n")
    return correct


try:
    start = time.time()
    import registration.models as mod
    from registration.models import market_chart
    for i in range(1, 26):
        price_list = []
        for curr in currencies:
            price = cg.get_coins_markets(
                vs_currency=curr, per_page="250", page=f"{i}", price_change_percentage="1h")
            price_list += price
        for j in range(250):
            cryptoObject = mod.cryptoObject(coin_id=price_list[j]["id"], symbol=price_list[j]["symbol"],
                                            name=price_list[j]["name"], image=price_list[j]["image"],
                                            last_updated=correcttime(price_list[j]["last_updated"]))
            cryptoObject.save()
            for k in range(4):
                coinFromList = price_list[j+(250*k)]
                try:
                    last_value = mod.value.objects.filter(currency=currencies[k]).get(
                        coin__coin_id=price_list[j]["id"]).current
                except:
                    last_value=0
                crypto_value = mod.value(coin_currency=f"{price_list[j]['id']}_{currencies[k]}",
                                         coin=cryptoObject,
                                         currency=currencies[k],
                                         current=coinFromList["current_price"],
                                         last_price=last_value if last_value is not None else None,
                                         high_1d=coinFromList["high_24h"],
                                         low_1d=coinFromList["low_24h"],
                                         ath=coinFromList["ath"],
                                         ath_time=correcttime(
                                             coinFromList["ath_date"]),
                                         atl=coinFromList["ath"],
                                         atl_time=correcttime(
                                             coinFromList["atl_date"]),
                                         percentage_1d=coinFromList["price_change_percentage_24h"],
                                         percentage_1h=coinFromList["price_change_percentage_24h"])
                crypto_value.save()
except:
    traceback.print_exc()
finally:
    print(f"{datetime.datetime.now()} {round(time.time()-start, 2)}")
