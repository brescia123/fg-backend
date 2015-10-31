from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    name = models.CharField(max_length=70)
    role = models.CharField(max_length=1)
    team = models.ForeignKey(Team, null=True, blank=True)
    price = models.IntegerField(default=1)
    attendances = models.IntegerField(default=0)
    gol = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    penalties_kicked = models.IntegerField(default=0)
    penalties_scored = models.IntegerField(default=0)
    penalties_missed = models.IntegerField(default=0)
    penalties_saved = models.IntegerField(default=0)
    vote_avg = models.FloatField(default=0.0)
    magicvote_avg = models.FloatField(default=0.0)
    seriea = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Vote(models.Model):
    player = models.ForeignKey(Player)
    vote = models.FloatField(default=0.0)
    gol = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    penalties_scored_saved = models.IntegerField(default=0)
    penalties_missed = models.IntegerField(default=0)
    own_gol = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    magicvote = models.FloatField(default=0.0)
    day = models.IntegerField(default=0)
    sub_in = models.BooleanField(default=False)
    sub_out = models.BooleanField(default=False)

    def __unicode__(self):
        return self.player.name


class UpdateRun(models.Model):
    run_date = models.DateField(auto_now_add=True)
    duration = models.FloatField()
    no_new_votes = models.IntegerField(default=0)
    no_new_players = models.IntegerField(default=0)
    no_new_orphans = models.IntegerField(default=0)

    def __unicode__(self):
        return ('Update summury:\n'
                ' Date - ' + self.run_date.strftime('%d/%b/%y %H.%M.%S') + '\n'
                ' Duration - %.1f' % (self.duration) + '\n'
                ' New Votes: - %i' % (self.no_new_votes) + '\n'
                ' New Players - %i' % (self.no_new_players) + '\n'
                ' New Orphans - %i' % (self.no_new_orphans) + '\n')
