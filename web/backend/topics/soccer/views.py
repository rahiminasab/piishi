from web.backend.base.views import *
from .models import *


class SoccerTournamentListView(EventSetListView):
    model = SoccerTournament
