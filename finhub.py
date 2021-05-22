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
    from registration.models import CompanyProfile
    from registration.models import StockPrices
    import time

    token = 'c2kesraad3i96dg8avc0'

    r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token='+token)
    #print(r.json()[0]['symbol'])
    tickers = r.json()
    j = 0
    for i in tickers:
        if j==9:
            time.sleep(2)
            j=0
        symbol = i['symbol']
        r = requests.get('https://finnhub.io/api/v1/stock/profile2?symbol='+symbol+'&token='+token) # company info
        values = r.json()
        if not bool(values):
            continue
        print(values)
        companyProfile = CompanyProfile(country = values['country'] if values['country'] is not None else 'N/A',
                                        company_name = values['name'] if values['name'] is not None else 'N/A',
                                        symbol = values['ticker'] if values['ticker'] is not None else 'N/A',
                                        date_founded = correcttime(values['ipo']) ,
                                        weburl = values['weburl'] if values['weburl'] is not None else 'N/A',
                                        logo = values['logo'] if values['logo'] is not None else 'N/A',
                                        exchange = values['exchange'] if values['exchange'] is not None else 'N/A',
                                        market_cap = values['marketCapitalization'] if values['marketCapitalization'] is not None else 0,
                                        shareOutstanding = values['shareOutstanding'] if values['shareOutstanding'] is not None else 0,
                                        finnhubIndustry = values['finnhubIndustry'] if values['finnhubIndustry'] is not None else 0)
        companyProfile.save()
        z = requests.get('https://finnhub.io/api/v1/quote?symbol='+i['symbol']+'&token='+token) # stock info quoutes
        values = z.json()
        stockPrices = StockPrices(symbol = companyProfile,
                                  closed= values['c'],
                                  high24= values['h'],
                                  low24 = values['l'],
                                  open = values['o'],
                                  previous_closed = values['pc'])
        stockPrices.save()
        j+=1
        print(values)
except:
    traceback.print_exc()


