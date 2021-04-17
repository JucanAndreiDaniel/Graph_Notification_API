# Generated by Django 3.2 on 2021-04-17 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_alter_value_coin_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='value',
            name='id',
        ),
        migrations.AddField(
            model_name='value',
            name='coin_currency',
            field=models.CharField(blank=True, max_length=255, primary_key=True, serialize=False),
        ),
    ]