from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.json import HasKeyLookup
from django.db.models.fields.related import ForeignKey


class cryptoObject(models.Model):

    coin_id = models.CharField(max_length=255, primary_key=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    last_updated = models.DateTimeField(7)


class value(models.Model):
    coin_currency = models.CharField(
        max_length=255, primary_key=True)
    coin = models.ForeignKey(cryptoObject, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255)

    percentage_1h = models.FloatField(blank=True, null=True)
    percentage_1d = models.FloatField(blank=True, null=True)

    current = models.FloatField(blank=True, null=True)
    last_price = models.FloatField(blank=True, null=True)
    
    high_1d = models.FloatField(blank=True, null=True)
    low_1d = models.FloatField(blank=True, null=True)

    ath = models.FloatField(blank=True, null=True)
    ath_time = models.DateTimeField(7)

    atl = models.FloatField(blank=True, null=True)
    atl_time = models.DateTimeField(7)


class market_chart(models.Model):
    coin_currency_day = models.CharField(
        max_length=255, primary_key=True)
    coin = models.ForeignKey(cryptoObject, on_delete=models.CASCADE)
    currency = models.CharField(max_length=255)

    class Days(models.TextChoices):
        ONE = '1', ('1')
        TWO = '2', ('2')
        THREE = '3', ('3')
        FOUR = '4', ('4')
        FIVE = '5', ('5')
        SIX = '6', ('6')
        SEVEN = '7', ('7')

    day = models.CharField(
        max_length=255, choices=Days.choices, default=Days.ONE)

    price1 = models.FloatField(blank=True, null=True)
    price2 = models.FloatField(blank=True, null=True)
    price3 = models.FloatField(blank=True, null=True)
    price4 = models.FloatField(blank=True, null=True)
    price5 = models.FloatField(blank=True, null=True)
    price6 = models.FloatField(blank=True, null=True)
    price7 = models.FloatField(blank=True, null=True)
    price8 = models.FloatField(blank=True, null=True)
    price9 = models.FloatField(blank=True, null=True)
    price10 = models.FloatField(blank=True, null=True)
    price11 = models.FloatField(blank=True, null=True)
    price12 = models.FloatField(blank=True, null=True)
    price13 = models.FloatField(blank=True, null=True)
    price14 = models.FloatField(blank=True, null=True)
    price15 = models.FloatField(blank=True, null=True)
    price16 = models.FloatField(blank=True, null=True)
    price17 = models.FloatField(blank=True, null=True)
    price18 = models.FloatField(blank=True, null=True)
    price19 = models.FloatField(blank=True, null=True)
    price20 = models.FloatField(blank=True, null=True)
    price21 = models.FloatField(blank=True, null=True)
    price22 = models.FloatField(blank=True, null=True)
    price23 = models.FloatField(blank=True, null=True)
    price24 = models.FloatField(blank=True, null=True)


class Notification(models.Model):
    coin = models.ForeignKey(cryptoObject, on_delete=models.CASCADE)
    value_type = models.CharField(
        max_length=255, default="bigger")  # Value or percentage
    # target_type = models.CharField(max_length=255,default=">") # Mai mare sau mai mic
    initial_value = models.FloatField(default=0)
    final_value = models.FloatField()
    enabled = models.BooleanField(default=True)
    via_mail = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    favorite = models.ManyToManyField(cryptoObject)
    notification = models.ManyToManyField(Notification)
    fav_currency = models.CharField(max_length=255, blank=True, default="eur")


class CompanyProfile(models.Model):
    country = models.CharField(max_length=255, default='N/A')
    exchange = models.CharField(max_length=255, default='N/A')
    date_founded = models.DateField(7)
    market_cap = models.IntegerField(default = 0)
    company_name = models.CharField(max_length=255, default='N/A')
    shareOutstanding = models.FloatField(default = 0)
    symbol = models.CharField(max_length=255, primary_key=True)
    weburl = models.CharField(max_length=255, default='N/A')
    logo = models.CharField(max_length = 255, default='N/A')
    finnhubIndustry = models.CharField(max_length = 255, default='N/A')


class StockPrices(models.Model):
    symbol = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, primary_key=True)
    closed = models.FloatField()
    high24 = models.FloatField()
    low24 = models.FloatField()
    open = models.FloatField()
    previous_closed = models.FloatField()