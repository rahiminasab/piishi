from web.backend.base.models import *


class LeagueTournament(EventSet):
    class Meta(EventSet.Meta):
        db_table = 'psh_soccer_league_tournament'

    number_of_teams = models.PositiveIntegerField()


class KnockOutTournament(EventSet):
    class Meta(EventSet.Meta):
        db_table = 'psh_soccer_knockout_tournament'

    number_of_teams = models.PositiveIntegerField()


class MixedTournament(EventSet):
    class Meta(EventSet.Meta):
        db_table = 'psh_soccer_mixed_tournament'

    number_of_teams = models.PositiveIntegerField()


class SoccerTeam(models.Model):
    class Meta:
        db_table = 'psh_soccer_team'

    name = models.CharField(max_length=100)
    fifa_code = models.CharField(max_length=10, null=True, blank=True)
    iso2 = models.CharField(max_length=3, null=True, blank=True)
    flag = models.URLField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class SoccerMatch(Event):
    class Meta(Event.Meta):
        db_table = 'psh_soccer_match'

    home_team = models.ForeignKey(SoccerTeam, on_delete=models.PROTECT)
    away_team = models.ForeignKey(SoccerTeam, on_delete=models.PROTECT)
    home_result = models.PositiveIntegerField(null=True, blank=True)
    away_result = models.PositiveIntegerField(null=True, blank=True)
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(SoccerTeam, null=True, blank=True, on_delete=models.PROTECT)

    def __unicode__(self):
        return "%s vs %s".format(self.home_team, self.away_team)


class SoccerMatchPrediction(Prediction):
    class Meta(Prediction.Meta):
        db_table = 'psh_soccer_prediction'

    home_result = models.PositiveIntegerField()
    away_result = models.PositiveIntegerField()
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(SoccerTeam, null=True, blank=False, on_delete=models.PROTECT)

    def __unicode__(self):
        return "%s-%s: %s-%s".format(self.foreteller, self.event, self.home_result, self.away_result)
