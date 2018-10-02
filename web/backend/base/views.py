from django.views.generic import ListView
from .models import *


class EventSetListView(ListView):
    model = EventSet