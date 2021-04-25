# Generated by Django 3.2 on 2021-04-25 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='cryptoObject',
            fields=[
                ('coin_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('last_updated', models.DateTimeField(verbose_name=7)),
            ],
        ),
        migrations.CreateModel(
            name='value',
            fields=[
                ('coin_currency', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('currency', models.CharField(max_length=255)),
                ('current', models.FloatField(blank=True, null=True)),
                ('high_1d', models.FloatField(blank=True, null=True)),
                ('low_1d', models.FloatField(blank=True, null=True)),
                ('ath', models.FloatField(blank=True, null=True)),
                ('ath_time', models.DateTimeField(verbose_name=7)),
                ('atl', models.FloatField(blank=True, null=True)),
                ('atl_time', models.DateTimeField(verbose_name=7)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.cryptoobject')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('favorite', models.ManyToManyField(to='registration.cryptoObject')),
            ],
        ),
    ]
