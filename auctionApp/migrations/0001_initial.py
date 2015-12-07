# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('price', models.FloatField(default=0)),
                ('date', models.DateTimeField(verbose_name='the day the bid was made')),
            ],
        ),
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=80)),
                ('starting_bid', models.FloatField(default=0)),
                ('buyoff_price', models.FloatField(default=0)),
                ('expires', models.DateTimeField(verbose_name='the day the bidding ends')),
                ('bought', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Trader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('information', models.TextField(blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='trader',
            field=models.ForeignKey(to='auctionApp.Trader'),
        ),
        migrations.AddField(
            model_name='bid',
            name='buyer',
            field=models.ForeignKey(to='auctionApp.Buyer'),
        ),
        migrations.AddField(
            model_name='bid',
            name='lot',
            field=models.ForeignKey(to='auctionApp.Lot'),
        ),
    ]
