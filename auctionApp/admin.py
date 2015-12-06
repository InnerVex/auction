from django.contrib import admin

from auctionApp.models import Trader
from auctionApp.models import Buyer
from auctionApp.models import Lot
from auctionApp.models import Bid


class BidInline(admin.TabularInline):
    model = Bid
    extra = 1

class LotInline(admin.TabularInline):
    model = Lot
    extra = 1

class LotAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields' : ['name', 'trader']}),
        ('Bidding', {'fields' : ['starting_bid', 'buyoff_price', 'expires', 'bought']})
    )
    list_display = ('name', 'expires')
    search_fields = ['name']
    inlines = [BidInline]

class BuyerAdmin(admin.ModelAdmin):
    inlines = [BidInline]

class TraderAdmin(admin.ModelAdmin):
    inlines = [LotInline]

admin.site.register(Trader, TraderAdmin)
admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Lot, LotAdmin)
admin.site.register(Bid)
