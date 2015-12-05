from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registration/', views.registration, name='registration'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/', views.login_action, name='login'),
    url(r'^logout/', views.logout_action, name='logout'),
    url(r'^create_lot/', views.create_lot, name='create_lot'),
    url(r'^change_lot/', views.change_lot, name='change_lot'),
    url(r'^delete_lot/', views.delete_lot, name='delete_lot'),
    url(r'^make_bid/', views.make_bid, name='make_bid'),
    url(r'^buy_off/', views.buy_off, name='buy_off')
]
