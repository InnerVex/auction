from django.test import TestCase

from django.contrib.auth.models import User
from auctionApp.views import search_lots, is_user_logged, show_info, change_lot_inner
from auctionApp.models import Lot, Trader
from django.utils import timezone
from django.test.client import RequestFactory
from unittest.mock import patch


class TestDefs(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_search_lots(self):
        with patch('auctionApp.views.is_user_logged') as mock_logged:
            mock_logged.return_value = True

            request = self.factory.get('/')
            request.POST._mutable = True
            request.POST['search_name'] = 'picture'
            request.POST['trader_id'] = 1
            request.POST['own'] = 'on'

            user1 = User.objects.create_user('user1', 'user1@user.ru', 'user1')
            user2 = User.objects.create_user('user2', 'user2@user.ru', 'user2')
            trader1 = Trader.objects.create(user=user1, information='hello1')
            trader2 = Trader.objects.create(user=user2, information='hello2')
            Lot.objects.create(expires=timezone.now(), name='picture creator', trader=trader1)
            Lot.objects.create(expires=timezone.now(), name='picture destroyer', trader=trader2)

            self.assertListEqual(
                list(search_lots(request)),
                list(Lot.objects.filter(name__icontains='picture').filter(trader__pk=1).order_by('-expires')))

    def test_is_user_logged(self):
        request = self.factory.get('/')
        self.assertFalse(is_user_logged(request))

    def test_show_info(self):
        user1 = User.objects.create_user('user1', 'user1@user.ru', 'user1')
        user2 = User.objects.create_user('user2', 'user2@user.ru', 'user2')
        Trader.objects.create(user=user1, information='oh uh')
        Trader.objects.create(user=user2, information='hello, it is the RIGHT one')

        self.assertEqual(show_info(2), 'hello, it is the RIGHT one')

    def test_change_lot_inner(self):
        user1 = User.objects.create_user('user1', 'user1@user.ru', 'user1')
        trader1 = Trader.objects.create(user=user1, information='hello1')
        Lot.objects.create(expires=timezone.now(), name='OLD NAME', trader=trader1)

        request = self.factory.get('/')
        request.POST._mutable = True
        request.POST['lot_id'] = 1
        request.POST['name'] = 'NEW NAME'
        request.POST['buyoff_price'] = 100
        request.POST['starting_bid'] = 10
        request.POST['expires'] = timezone.now()

        change_lot_inner(request)
        lot_to_check = Lot.objects.get(pk=request.POST['lot_id'])

        self.assertEqual(lot_to_check.name, 'NEW NAME')
