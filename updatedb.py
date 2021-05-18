
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
                vs_currency=curr, per_page="250", page=f"{i}", sparkline="true", price_change_percentage="1h")
            price_list += price
        for j in range(250):
            cryptoObject = mod.cryptoObject(coin_id=price_list[j]["id"], symbol=price_list[j]["symbol"],
                                            name=price_list[j]["name"], image=price_list[j]["image"],
                                            last_updated=correcttime(price_list[j]["last_updated"]))
            cryptoObject.save()
            for k in range(4):
                coinFromList = price_list[j+(250*k)]
                crypto_value = mod.value(coin_currency=f"{price_list[j]['id']}_{currencies[k]}",
                                         coin=cryptoObject,
                                         currency=currencies[k],
                                         current=coinFromList["current_price"],
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
                for l in range(1, 8):
                    try:
                        crypto_market = mod.market_chart(coin_currency_day=f"{price_list[j]['id']}_{currencies[k]}_{(l-1)}",
                                                         coin=cryptoObject,
                                                         currency=currencies[k],
                                                         day=market_chart.Days(
                                                             f"{l}"),
                                                         price1=coinFromList["sparkline_in_7d"]["price"][0+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price2=coinFromList["sparkline_in_7d"]["price"][1+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price3=coinFromList["sparkline_in_7d"]["price"][2+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price4=coinFromList["sparkline_in_7d"]["price"][3+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price5=coinFromList["sparkline_in_7d"]["price"][4+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price6=coinFromList["sparkline_in_7d"]["price"][5+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price7=coinFromList["sparkline_in_7d"]["price"][6+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price8=coinFromList["sparkline_in_7d"]["price"][7+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price9=coinFromList["sparkline_in_7d"]["price"][8+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price10=coinFromList["sparkline_in_7d"]["price"][9+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price11=coinFromList["sparkline_in_7d"]["price"][10+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price12=coinFromList["sparkline_in_7d"]["price"][11+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price13=coinFromList["sparkline_in_7d"]["price"][12+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price14=coinFromList["sparkline_in_7d"]["price"][13+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price15=coinFromList["sparkline_in_7d"]["price"][14+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price16=coinFromList["sparkline_in_7d"]["price"][15+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price17=coinFromList["sparkline_in_7d"]["price"][16+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price18=coinFromList["sparkline_in_7d"]["price"][17+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price19=coinFromList["sparkline_in_7d"]["price"][18+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price20=coinFromList["sparkline_in_7d"]["price"][19+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price21=coinFromList["sparkline_in_7d"]["price"][20+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price22=coinFromList["sparkline_in_7d"]["price"][21+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price23=coinFromList["sparkline_in_7d"]["price"][22+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         price24=coinFromList["sparkline_in_7d"]["price"][23+(
                                                             24*(int(market_chart.Days(f"{l}").value)-2))],
                                                         )
                    except Exception as e:
                        pass
                    finally:
                        crypto_market.save()

except:
    traceback.print_exc()
finally:
    print(f"{datetime.datetime.now()} {round(time.time()-start, 2)}")
