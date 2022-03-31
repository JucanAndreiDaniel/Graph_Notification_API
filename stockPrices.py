import django
import os
import traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'login_api.settings')


django.setup()


def correcttime(timestamp: str):
    if timestamp == '':
        correct = "2000-01-01"
        return correct
    return timestamp


try:

    import requests
    from oldAPI.models import CompanyProfile
    from oldAPI.models import StockPrices
    import time

    token = os.environ.get('TOKEN_FINHUB')
    tickers = CompanyProfile.objects.all()
    j = 0
    for i in tickers:
        if j == 9:
            time.sleep(2)
            j = 0
        # stock info quoutes
        z = requests.get(
            f'https://finnhub.io/api/v1/quote?symbol={i.symbol}&token={token}')
        values = z.json()
        try:
            if values['error']:
                continue
        except:
            pass
        stockPrices = StockPrices(symbol=i,
                                  closed=values['c'],
                                  high24=values['h'],
                                  low24=values['l'],
                                  open=values['o'],
                                  previous_closed=values['pc'])
        stockPrices.save()
        j += 1
        print(values)
except:
    traceback.print_exc()
