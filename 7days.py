from pycoingecko import CoinGeckoAPI
import time

cg = CoinGeckoAPI()

allCoins = cg.get_coins_list()  # get all coins
                                # the function returns a list of dicts 
                                # with id,name and something 


idList = list() # create a new list 
for i in allCoins: # iterate in list of dicts 
    idList.append(i['id']) # we need only the coin id to be added in the new list 


usd = list()
eur = list()
rub = list()
gbp = list()

cur = ["usd", "eur", "rub", "gbp"]
# toReturn = [usd, eur, rub, gbp]




for currency in cur: # for every currency
    finalDic = {}
    for cID in idList:# for every coin ID
        sevenDays = cg.get_coin_market_chart_by_id(id=cID, interval='hourly', vs_currency=currency, days='7') # get market chart which returns a dict with 'prices' (it contains market cap and the actual price on position 1)
        onlyP = list()
        for entrys in sevenDays['prices']: # iterate in dict by key 'prices' and take the second value of each
            onlyP.append(entrys[1]) # add it in a list 
        finalDic[cID] = onlyP # add the list of prices in dict with value of key the coin id and the value is a list of values
    # add every final dict in a list named after currency 
    if cur == 'usd':
        usd.append(finalDic) 
    if cur == 'eur':
        eur.append(finalDic)
    if cur == 'rub':
        rub.append(finalDic)
    if cur == 'gbp':
        gbp.append(finalDic)


