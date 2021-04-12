from django.db import models
from django.contrib.auth.models import User


class crypto_id(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    high_24 = models.IntegerField()
    low_24 = models.IntegerField()
    curr_usd = models.IntegerField()
    curr_euro = models.IntegerField()
    curr_gbp = models.IntegerField()
    curr_rub = models.IntegerField()
    ath_usd = models.IntegerField()
    ath_euro = models.IntegerField()
    ath_gbp = models.IntegerField()
    ath_rub = models.IntegerField()
    atl_usd = models.IntegerField()
    atl_euro = models.IntegerField()
    atl_gbp = models.IntegerField()
    atl_rub = models.IntegerField()
    ath_time = models.TimeField(7)
    atl_time = models.TimeField(7)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    favorite = models.ManyToManyField(crypto_id)
