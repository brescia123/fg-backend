from django.contrib import admin
from models import Team, Player, Vote


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'modified')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'team', 'price', 'attendances', 'gol',
                    'assist', 'yellow_cards', 'red_cards', 'penalties_kicked',
                    'penalties_scored', 'penalties_missed', 'penalties_saved',
                    'vote_avg', 'magicvote_avg', 'seriea', 'created',
                    'modified')


class VoteAdmin(admin.ModelAdmin):
    list_display = ('player', 'vote', 'gol', 'assist',
                    'penalties_scored_saved', 'penalties_missed', 'own_gol',
                    'yellow_cards', 'red_cards', 'magicvote', 'day', 'sub_in',
                    'sub_out', 'created', 'modified')

admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Vote, VoteAdmin)
