from django.db import models
from django.contrib.auth.models import User


class crypto_id(models.Model):

    id = models.CharField(max_length=255, primary_key=True)
    symbol = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)

    high_1d_usd = models.FloatField(blank=True, null=True)
    high_1d_euro = models.FloatField(blank=True, null=True)
    high_1d_gbp = models.FloatField(blank=True, null=True)
    high_1d_rub = models.FloatField(blank=True, null=True)

    low_1d_usd = models.FloatField(blank=True, null=True)
    low_1d_euro = models.FloatField(blank=True, null=True)
    low_1d_gbp = models.FloatField(blank=True, null=True)
    low_1d_rub = models.FloatField(blank=True, null=True)

    curr_usd = models.FloatField(blank=True, null=True)
    curr_euro = models.FloatField(blank=True, null=True)
    curr_gbp = models.FloatField(blank=True, null=True)
    curr_rub = models.FloatField(blank=True, null=True)

    ath_usd = models.FloatField(blank=True, null=True)
    ath_euro = models.FloatField(blank=True, null=True)
    ath_gbp = models.FloatField(blank=True, null=True)
    ath_rub = models.FloatField(blank=True, null=True)

    atl_usd = models.FloatField(blank=True, null=True)
    atl_euro = models.FloatField(blank=True, null=True)
    atl_gbp = models.FloatField(blank=True, null=True)
    atl_rub = models.FloatField(blank=True, null=True)
    ath_time = models.DateTimeField(7)
    atl_time = models.DateTimeField(7)

    last_updated = models.DateTimeField(7)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    favorite = models.ManyToManyField(crypto_id)
