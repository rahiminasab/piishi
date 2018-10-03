from django.contrib import admin
from web.backend.models import *


class TopicAdmin(admin.ModelAdmin):
    pass


class SoccerTournamentAdmin(admin.ModelAdmin):
    pass


class SoccerMatchAdmin(admin.ModelAdmin):
    pass


class SoccerMatchPredictionAdmin(admin.ModelAdmin):
    pass


class SoccerTeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Topic, TopicAdmin)

admin.site.register(SoccerTournament, SoccerTournamentAdmin)
admin.site.register(SoccerMatch, SoccerMatchAdmin)
admin.site.register(SoccerMatchPrediction, SoccerMatchPredictionAdmin)
admin.site.register(SoccerTeam, SoccerTeamAdmin)
