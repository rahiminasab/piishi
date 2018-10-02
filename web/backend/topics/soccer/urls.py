from django.urls import path, re_path
from .views import SoccerTournamentListView


url_patterns = [
    path('soccer/tournaments', SoccerTournamentListView.as_view(), name='soccer_tournaments')
]