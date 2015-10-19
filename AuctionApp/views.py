from django.views.generic.list import ListView
from auctionApp.models import Lot

# Create your views here.
class LotListView(ListView):
    model = Lot