from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    id = models.CharField(max_length=70, primary_key=True)
    name = models.CharField(max_length=70)
    role = models.CharField(max_length=1)
    team = models.ForeignKey(Team)
    price = models.IntegerField(default=1)
    attendances = models.IntegerField(default=0)
    gol = models.IntegerField(default=0)
    assist = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    penalties_kicked = models.IntegerField(default=0)
    penalties_missed = models.IntegerField(default=0)
    penalties_saved = models.IntegerField(default=0)
    vote_avg = models.FloatField(default=0.0)
    magicvote_avg = models.FloatField(default=0.0)

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

    def __unicode__(self):
        return self.player.name
