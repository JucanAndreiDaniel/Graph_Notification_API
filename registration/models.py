from django.db import models
from django.contrib.auth.models import User


class crypto_id(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    last_updated = models.DateTimeField(7)


class value(models.Model):

    currency_list = (("usd", "Dollar"), ("eur", "Euro"),
                     ("gbp", "Pound"), ("rub", "Ruble"))

    coin_currency = models.CharField(
        max_length=255, primary_key=True, blank=True)
    coin_id = models.ForeignKey(
        crypto_id, on_delete=models.CASCADE, related_name="prices")
    currency = models.CharField(
        max_length=255, choices=currency_list)

    current = models.FloatField(blank=True, null=True)
    high_1d = models.FloatField(blank=True, null=True)
    low_1d = models.FloatField(blank=True, null=True)

    ath = models.FloatField(blank=True, null=True)
    ath_time = models.DateTimeField(7)

    atl = models.FloatField(blank=True, null=True)
    atl_time = models.DateTimeField(7)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    favorite = models.ManyToManyField(crypto_id)
