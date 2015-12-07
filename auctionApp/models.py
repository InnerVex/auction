from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Trader(models.Model):
    user = models.ForeignKey(User, default=User.objects.create_user('delete_me', 'delete_me@delete_me.ru', 'delete_me'))
    information = models.TextField(blank=True)

    def __str__(self):
        return str(self.user)


class Buyer(models.Model):
    user = models.ForeignKey(User, default=User.objects.create_user('delete_me', 'delete_me@delete_me.ru', 'delete_me'))

    def __str__(self):
        return str(self.user)


class Lot(models.Model):
    trader = models.ForeignKey(Trader, default=Trader.objects.create())
    name = models.CharField(max_length=80, default='default_name')
    starting_bid = models.FloatField(default=0)
    buyoff_price = models.FloatField(default=0)
    expires = models.DateTimeField('the day the bidding ends', default=timezone.now())
    bought = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def current_bid(self):
        try:
            bid = Bid.objects.filter(lot__pk=self.pk).latest(field_name='date')
        except Bid.DoesNotExist:
            buyer = Buyer.objects.get(pk=1)
            bid = Bid.objects.create(lot=self, buyer=buyer, price=self.starting_bid, date=timezone.now())
            bid.save()
        return bid


class Bid(models.Model):
    lot = models.ForeignKey(Lot, default=Lot.objects.create())
    buyer = models.ForeignKey(Buyer, default=Buyer.objects.create())
    price = models.FloatField(default=0)
    date = models.DateTimeField('the day the bid was made', default=timezone.now())

    def __str__(self):
        return '{} wants to buy {} for {}'.format(self.buyer, self.lot, self.price)
