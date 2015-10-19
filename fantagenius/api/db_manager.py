from models import Player, Vote, Team
from django.conf import settings
import re
import json
import urllib
import os


def init_teams():
    '''
    Initialize the Team table with the team names retrieved from Kimono
    '''
    url = settings.KIMONO['teams_url']
    key = os.environ.get('KIMONO_API_KEY')
    results = json.load(urllib.urlopen(url + '?apikey=' + key))['results']
    teams = results['collection1']
    teams_name = [team['name'] for team in teams]
    for team_name in teams_name:
        if not Team.objects.filter(name__iexact=team_name).exists():
            t = Team()
            t.name = team_name
            t.save()


def update_players(players_json):
    '''
    Used to update the Player table with the json retrieved from Kimono.
    If a player is not in the table it creates one.
    '''
    url = settings.KIMONO['players_url']
    key = os.environ.get('KIMONO_API_KEY')
    results = json.load(urllib.urlopen(url + '?apikey=' + key))['results']
    players = results['collection1']
    for player in players:
        p = Player()
        # Using the last token of the URL as the pimary key
        # If the player is already in the db, using the same pk end up updating
        # the past value
        p.id = player['name']['href'].split('/')[-1]
        p.name = player['name']['text']
        # Converting 'T (C)' or 'T (A)' to 'A' or 'C'
        p.role = re.sub('[^PDCA]', '', player['role'])
        p.team = Team.objects.get(name__iexact=player['team'])
        p.price = player['price']
        # Replacing the '-' character with 0 in remaining fields
        p.attendances = player['attendances'].replace('-', '0')
        p.gol = player['gol'].replace('-', '0')
        p.assist = player['assist'].replace('-', '0')
        p.yellow_cards = player['yellow_cards'].replace('-', '0')
        p.red_cards = player['red_cards'].replace('-', '0')
        p.penalties_kicked = player['penalties_kicked'].replace('-', '0')
        p.penalties_missed = player['penalties_missed'].replace('-', '0')
        p.penalties_saved = player['penalties_saved'].replace('-', '0')
        p.vote_avg = player['vote_avg'].replace('-', '0')
        p.magicvote_avg = player['magicvote_avg'].replace('-', '0')
        # Storing on the db
        p.save()
