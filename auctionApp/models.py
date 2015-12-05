from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Trader(models.Model):
    user = models.ForeignKey(User)
    information = models.TextField(blank=True)

    def __str__(self):
        return str(self.user)


class Buyer(models.Model):
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.user)


class Lot(models.Model):
    trader = models.ForeignKey(Trader)
    name = models.CharField(max_length=80)
    starting_bid = models.FloatField(default=0)
    buyoff_price = models.FloatField(default=0)
    expires = models.DateTimeField('the day the bidding ends')
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
    lot = models.ForeignKey(Lot)
    buyer = models.ForeignKey(Buyer)
    price = models.FloatField(default=0)
    date = models.DateTimeField('the day the bid was made')

    def __str__(self):
        return '{} wants to buy {} for {}'.format(self.buyer, self.lot, self.price)
