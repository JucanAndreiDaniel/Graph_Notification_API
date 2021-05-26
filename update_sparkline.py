
from pycoingecko import CoinGeckoAPI
import django
import os
import traceback
from statistics import mean

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')


django.setup()


def correcttime(timestamp: str):
    try:
        timestamplist = timestamp.split("T")
        correct = timestamplist[0]+" "+timestamplist[1][:-2]+"+00:00"
    except:
        correct = "2000-01-01 00:00:00+00:00"
        print(f"{timestamp}\n")
    return correct


cg = CoinGeckoAPI()

currencies = ["usd", "eur", "gbp", "rub"]

try:
    from registration.models import market_chart, cryptoObject
    for i in range(1, 26):
        price_list = []
        for curr in currencies:
            price = cg.get_coins_markets(
                vs_currency=curr, per_page="250", page=f"{i}", sparkline="true")
            price_list += price
        for j in range(250):
            cryptoobject = cryptoObject(coin_id=price_list[j]["id"], symbol=price_list[j]["symbol"],
                                            name=price_list[j]["name"], image=price_list[j]["image"],
                                            last_updated=correcttime(price_list[j]["last_updated"]))
            cryptoobject.save()
            for k in range(4):
                coinFromList = price_list[j+(250*k)]
                for l in range(1, 8):
                    try:
                        prices = []
                        for price in range(24):
                            prices.append(coinFromList["sparkline_in_7d"]["price"][price+(
                                                            24*(int(market_chart.Days(f"{l}").value)-2))])
                        crypto_market = market_chart(coin_currency_day=f"{price_list[j]['id']}_{currencies[k]}_{(l-1)}",
                                                        coin=cryptoobject,
                                                        currency=currencies[k],
                                                        day=market_chart.Days(
                                                            f"{l}"),
                                                        price1=prices[0],
                                                        price2=prices[1],
                                                        price3=prices[2],
                                                        price4=prices[3],
                                                        price5=prices[4],
                                                        price6=prices[5],
                                                        price7=prices[6],
                                                        price8=prices[7],
                                                        price9=prices[8],
                                                        price10=prices[9],
                                                        price11=prices[10],
                                                        price12=prices[11],
                                                        price13=prices[12],
                                                        price14=prices[13],
                                                        price15=prices[14],
                                                        price16=prices[15],
                                                        price17=prices[16],
                                                        price18=prices[17],
                                                        price19=prices[18],
                                                        price20=prices[19],
                                                        price21=prices[20],
                                                        price22=prices[21],
                                                        price23=prices[22],
                                                        price24=prices[23],
                                                        media=mean(prices))
                    except Exception as e:
                        traceback.print_exc()
                    finally:
                        crypto_market.save()
except Exception as e:
    traceback.print_exc()
