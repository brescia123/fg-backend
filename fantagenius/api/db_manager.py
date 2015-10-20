from models import Player, Vote, Team
from django.conf import settings
import re
import json
import urllib
import os


def update():
    if not Team.objects.getAll().exists():
        init_teams()
    update_players()
    update_votes()


def init_teams():
    '''
    Initialize the Team table with the team names retrieved from Kimono
    '''
    url = settings.KIMONO['teams_url']
    teams = _get_results_collection1(url)
    teams_name = [team['name'] for team in teams]
    for team_name in teams_name:
        if not Team.objects.filter(name__iexact=team_name).exists():
            t = Team()
            t.name = team_name
            t.save()


def update_players():
    '''
    Updates the Player table with the json retrieved from Kimono.
    If a player is not in the table it creates one.
    '''
    url = settings.KIMONO['players_url']
    players = _get_results_collection1(url)
    for player in players:
        p = Player()
        # If the player is already in the db, using the same pk end up updating
        # the past value
        p.id = _id_from_url(player['name']['href'])
        p.name = player['name']['text']
        # Converting 'T (C)' or 'T (A)' to 'A' or 'C'
        p.role = re.sub('[^PDCA]', '', player['role'])
        p.team = Team.objects.get(name__iexact=player['team'])
        p.price = player['price']
        # Replacing the '-' character with 0 in remaining fields
        p.attendances = _fix_zero(player['attendances'])
        p.gol = _fix_zero(player['gol'])
        p.assist = _fix_zero(player['assist'])
        p.yellow_cards = _fix_zero(player['yellow_cards'])
        p.red_cards = _fix_zero(player['red_cards'])
        p.penalties_kicked = _fix_zero(player['penalties_kicked'])
        p.penalties_missed = _fix_zero(player['penalties_missed'])
        p.penalties_saved = _fix_zero(player['penalties_saved'])
        p.vote_avg = _fix_zero(player['vote_avg'])
        p.magicvote_avg = _fix_zero(player['magicvote_avg'])
        # Storing on the db
        p.save()


def update_votes():
    '''
    Updates the Vote table with the json retrieved from Kimono.
    If a vote is not in the table it creates one.
    '''
    url = settings.KIMONO['votes_url']
    votes = _get_results_collection1(url)
    # Keeping a list of players with votes but not present in the Player table
    # so that they could be added later
    # TODO: complete not in seria players eith the values retrieved from the
    # votes
    for vote in votes:
        p_id = _id_from_url(vote['name']['href'])
        v_day = _day_from_url(vote['url'])
        # Checking if the vote already exists. If not, creates a new one, if it
        # exists it will get the current vote and update it
        try:
            v = Vote.objects.get(player__pk=p_id, day=v_day)
        except Player.DoesNotExist:
            v = Vote()
        try:
            p = Player.objects.get(pk=p_id)
        except Player.DoesNotExist:
            p = Player(pk=p_id)
            p.save()
        v.player = p
        v.vote = _fix_zero(vote['vote'])
        v.gol = _fix_zero(vote['gol'])
        v.assist = _fix_zero(vote['assists'])
        v.penalties_scored_saved = _fix_zero(vote['penalties_scored_saved'])
        v.penalties_missed = _fix_zero(vote['penalties_missed'])
        v.own_gol = _fix_zero(vote['own_gol'])
        v.yellow_cards = _fix_zero(vote['yellow_cards'])
        v.red_cards = _fix_zero(vote['red_cards'])
        v.magicvote = _fix_zero(vote['own_gol'])
        v.day = v_day
        v.sub_in = _sub_in(vote['in']['class'])
        v.sub_out = _sub_out(vote['out']['class'])
        # Storing on the db
        v.save()
    _update_orphan_players()


def _update_orphan_players():
    '''
    Finds the players with no team and updates their stats querying the votes
    table
    '''
    orphans = Player.objects.exclude(team__isnull=False)
    for p in orphans:
        p_votes = Vote.objects.filter()
        p.name = _name_from_id(p.id)
        p.save()


def _name_from_id(p_id):
    '''
    Uses the id to generate the name of the Player
    '''
    return ' '.join(p_id.split('_')[:-1]).title()


def _get_results_collection1(url):
    '''
    Given an url it returns the the array 'collection1' that is present in the
    results from Kimono
    '''
    key = os.environ.get('KIMONO_API_KEY')
    results = json.load(urllib.urlopen(url + '?apikey=' + key))['results']
    return results['collection1']


def _fix_zero(value):
    '''
    Replaces the character '-' with the '0'
    '''
    return value.replace('-', '0')


def _id_from_url(url):
    '''
    Uses the last token of the URL to generate the id to use as a primary key
    '''
    return url.split('/')[-1]


def _day_from_url(url):
    '''
    Uses the last token of the URL to generate the number of the day
    '''
    return url.split('/')[-1].split('-')[-1]


def _sub_in(sub_class):
    return "in" in sub_class


def _sub_out(sub_class):
    return "out" in sub_class
