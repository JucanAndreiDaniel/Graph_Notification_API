from django.db import models
from django.contrib.auth.models import User


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

    current = models.FloatField(blank=True, null=True)
    high_1d = models.FloatField(blank=True, null=True)
    low_1d = models.FloatField(blank=True, null=True)

    ath = models.FloatField(blank=True, null=True)
    ath_time = models.DateTimeField(7)

    atl = models.FloatField(blank=True, null=True)
    atl_time = models.DateTimeField(7)


class Notification(models.Model):
    coin = models.ForeignKey(cryptoObject, on_delete=models.CASCADE)
    value_type = models.CharField(
        max_length=255, default="bigger")  # Value or percentage
    # target_type = models.CharField(max_length=255,default=">") # Mai mare sau mai mic
    intial_value = models.FloatField()
    final_value = models.FloatField()
    enabled = models.BooleanField(default=True)
    via_mail = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    favorite = models.ManyToManyField(cryptoObject)
    notification = models.ManyToManyField(Notification)
    fav_currency = models.CharField(max_length=255, blank=True, default="eur")
