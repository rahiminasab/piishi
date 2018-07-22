from web.backend.base.models import *


class SoccerTournament(EventSet):
    LEAGUE = 0
    KNOCKOUT = 1
    MIXED = 2

    types = (
        (LEAGUE, "League Tournament"),
        (KNOCKOUT, "Knockout Tournament"),
        (MIXED, "Mixed Tournament"),
    )

    class Meta(EventSet.Meta):
        db_table = 'psh_soccer_tournament'

    number_of_teams = models.PositiveIntegerField()
    type = models.PositiveIntegerField(choices=types)


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
        verbose_name_plural = "Soccer matches"

    event_set = models.ForeignKey(SoccerTournament, related_name="matches", on_delete=models.PROTECT)
    home_team = models.ForeignKey(SoccerTeam, related_name="home_matches", on_delete=models.PROTECT)
    away_team = models.ForeignKey(SoccerTeam, related_name="away_matches", on_delete=models.PROTECT)
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

    event = models.ForeignKey(SoccerMatch, related_name="predictions", on_delete=models.CASCADE)
    home_result = models.PositiveIntegerField()
    away_result = models.PositiveIntegerField()
    home_penalty = models.PositiveIntegerField(null=True, blank=True)
    away_penalty = models.PositiveIntegerField(null=True, blank=True)
    winner = models.ForeignKey(SoccerTeam, null=True, blank=False, on_delete=models.PROTECT)

    def __unicode__(self):
        return "%s-%s: %s-%s".format(self.foreteller, self.event, self.home_result, self.away_result)
