from django.db.models import Q
from django.shortcuts import render, redirect
from auctionApp.models import Lot, Trader, Buyer, Bid
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.utils import timezone
from functools import reduce
import operator


#Вспомогательные функции для тестов
def search_lots(request):
    post = request.POST
    predicates = []
    if 'search_name' in post:
        predicates.append(Q(name__icontains = post['search_name']))
    if 'own' in post:
        if post['own'] == 'on' and is_user_logged(request):
            predicates.append(Q(trader__id = post['trader_id']))

    if predicates != [] :
        lot_list = Lot.objects.filter(reduce(operator.and_, predicates)).order_by('-expires')
    else:
        lot_list = Lot.objects.order_by('-expires')

    return lot_list

def show_info(trader_pk):
    trader = Trader.objects.get(pk = trader_pk)
    return trader.information

def is_user_logged(request):
    if hasattr(request, 'user'):
        if request.user.is_authenticated():
            return True
        else:
            return False
    else:
        return False

def change_lot_inner(request):
    lot = Lot.objects.get(pk=request.POST['lot_id'])
    lot.name = request.POST['name']
    lot.buyoff_price = request.POST['buyoff_price']
    lot.starting_bid = request.POST['starting_bid']
    lot.expires = request.POST['expires']
    lot.save()

#Actions
def index(request):
    lot_list = search_lots(request)

    for lot in lot_list:
        if lot.expires > timezone.now():
            lot.bought = True
            lot.save()

    user = None; trader = None; buyer = None
    if request.user.is_authenticated():
        user = request.user
        try:
            trader = Trader.objects.get(user__pk = user.pk)
        except Trader.DoesNotExist:
            trader = None
        try:
            buyer = Buyer.objects.get(user__pk = user.pk)
        except Buyer.DoesNotExist:
            buyer = None
    context = {
        'user': user,
        'trader': trader,
        'buyer': buyer,
        'lot_list': lot_list,
        'post': request.POST}

    return render(request, 'auctionApp/index.html', context)

def registration(request):
    return render(request, 'auctionApp/registration.html')

def register(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)

    if user is None:
        user = User.objects.create_user(username, request.POST['email'], password)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        if 'is_trader' not in request.POST:
            trader = Trader.objects.create(user=user, information='hello')
            trader.save()
        else:
            buyer = Buyer.objects.create(user=user)
            buyer.save()

    return redirect('index')

def login_action(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('index')

def logout_action(request):
    logout(request)
    return redirect('index')

def create_lot(request):
    trader = Trader.objects.get(pk = request.POST['trader_id'])
    lot = Lot.objects.create(
        trader=trader,
        name=request.POST['name'],
        buyoff_price=request.POST['buyoff_price'],
        starting_bid=request.POST['starting_bid'],
        expires=request.POST['expires'])
    lot.save()
    return redirect('index')

def change_lot(request):
    change_lot_inner(request)
    return redirect('index')

def delete_lot(request):
    lot = Lot.objects.get(pk=request.POST['lot_id'])
    lot.delete()
    return redirect('index')

def make_bid(request):
    lot = Lot.objects.get(pk=request.POST['lot_id'])
    buyer = Buyer.objects.get(pk=request.POST['buyer_id'])
    price = float(request.POST['price'])
    better_bid = False
    try:
        cur_bid = lot.current_bid()
        if(price > cur_bid.price):
            better_bid = True
    except Bid.DoesNotExist:
        better_bid = True
    if better_bid and price > lot.starting_bid and price < lot.buyoff_price:
        bid = Bid.objects.create(lot=lot, buyer=buyer, price=price, date=timezone.now())
        bid.save()
    return redirect('index')

def buy_off(request):
    lot = Lot.objects.get(pk=request.POST['lot_id'])
    buyer = Buyer.objects.get(pk=request.POST['buyer_id'])
    lot.bought = True
    lot.save()
    bid = Bid.objects.create(lot=lot, buyer=buyer, price=lot.buyoff_price, date=timezone.now())
    bid.save()
    return redirect('index')