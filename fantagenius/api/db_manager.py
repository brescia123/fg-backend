from models import Player, Vote, Team, UpdateRun
from django.conf import settings
from django.db.models import Count, Sum
import re
import json
import urllib
import os
import logging
import time

logger = logging.getLogger(__name__)


def update():
    logger.info('Starting database update...')
    start = time.time()
    init_teams()
    no_new_p = update_players()
    no_new_v, no_new_o = update_votes()
    update_orphan_players()
    end = time.time()
    duration = float('%.1f' % (end-start))
    update_run = UpdateRun(duration=duration,
                           no_new_votes=no_new_v,
                           no_new_players=no_new_p,
                           no_new_orphans=no_new_o)
    update_run.save()
    logger.info('Database updated!')
    logger.info(update_run)


def drop_db():
    Team.objects.all().delete()
    Player.objects.all().delete()
    Vote.objects.all().delete()


def init_teams():
    '''
    Initialize the Team table with the team names retrieved from Kimono.
    It removes all the entries and re-adds them.
    '''
    logger.info('Initializing teams...')
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
    Returns the number of new palyers added to the db
    '''
    logger.info('Updating players...')
    url = settings.KIMONO['players_url']
    players = _get_results_collection1(url)
    logger.info(' - Updating database...')
    no_new_players = 0
    for player in players:
        p = Player()
        # If the player is already in the db, using the same pk end up updating
        # the past value
        p.id = _id_from_url(player['name']['href'])
        if not Player.objects.filter(pk=p.id).exists():
            no_new_players += 1
        p.name = player['name']['text']
        p.role = _fix_role(player['role'])
        p.team = Team.objects.get(name__iexact=player['team'])
        p.price = player['price']
        # Replacing the '-' character with 0 in remaining fields
        p.attendances = _fix_zero(player['attendances'])
        p.gol = _fix_zero(player['gol'])
        p.assist = _fix_zero(player['assist'])
        p.yellow_cards = _fix_zero(player['yellow_cards'])
        p.red_cards = _fix_zero(player['red_cards'])
        p.penalties_kicked = _fix_zero(player['penalties_kicked'])
        p.penalties_scored = _fix_zero(player['penalties_scored'])
        p.penalties_missed = _fix_zero(player['penalties_missed'])
        p.penalties_saved = _fix_zero(player['penalties_saved'])
        p.vote_avg = _fix_zero(player['vote_avg'])
        p.magicvote_avg = _fix_zero(player['magicvote_avg'])
        # Storing on the db
        p.save()
    return no_new_players


def update_votes():
    '''
    Updates the Vote table with the json retrieved from Kimono.
    If a vote is not in the table it creates one.
    Returns the number of new votes and new orphan players added to the db
    '''
    logger.info('Updating votes...')
    url = settings.KIMONO['votes_url']
    votes = _get_results_collection1(url)
    # Keeping a list of players with votes but not present in the Player table
    # so that they could be added later
    logger.info(' - Updating database...')
    no_new_votes = 0
    no_new_orphans = 0
    for vote in votes:
        p_id = _id_from_url(vote['name']['href'])
        v_day = _day_from_url(vote['url'])
        # Checking if the vote already exists. If not, creates a new one, if it
        # exists it will get the current vote and update it
        try:
            v = Vote.objects.get(player__pk=p_id, day=v_day)
        except Vote.DoesNotExist:
            v = Vote()
            no_new_votes += 1
        # Creating a orphan player if there is not a player for this vote
        try:
            p = Player.objects.get(pk=p_id)
        except Player.DoesNotExist:
            p = Player(pk=p_id)
            p.role = _fix_role(vote['role'])
            p.save()
            no_new_orphans += 1
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
    return no_new_votes, no_new_orphans


def update_orphan_players():
    '''
    Finds players with no team and updates their stats querying the votes
    table
    '''
    orphans = Player.objects.exclude(team__isnull=False)
    for p in orphans:
        p.name = _name_from_id(p.id)
        p.seriea = False
        p.price = 0
        v = Vote.objects
        ag = v.filter(player__pk=p.id).aggregate(Count('pk'),
                                                 Sum('gol'),
                                                 Sum('assist'),
                                                 Sum('penalties_scored_saved'),
                                                 Sum('penalties_missed'),
                                                 Sum('own_gol'),
                                                 Sum('yellow_cards'),
                                                 Sum('red_cards'),
                                                 Sum('vote'),
                                                 Sum('magicvote'),)
        p.attendances = ag['pk__count']
        p.gol = ag['gol__sum']
        p.assist = ag['assist__sum']
        if p.role == 'P':
            p.penalties_saved = ag['penalties_scored_saved__sum']
        else:
            p.penalties_scored = ag['penalties_scored_saved__sum']
        p.penalties_missed = ag['penalties_missed__sum']
        p.own_gol = ag['own_gol__sum']
        p.yellow_cards = ag['yellow_cards__sum']
        p.red_cards = ag['red_cards__sum']
        p.vote = ag['vote__sum'] / p.attendances
        p.magicvote = ag['magicvote__sum'] / p.attendances
        p.save()


def _name_from_id(p_id):
    '''
    Uses the id to generate the name of the Player
    '''
    return ' '.join(p_id.split('_')[:-1]).title()


def _get_results_collection1(url, offset=0):
    '''
    Given an url it returns the the array 'collection1' that is present in the
    results from Kimono
    Kimono has a result limit of 2500 rows. If that limit is reached
    it recursively calls the API with increasing offsets
    '''
    logger.info(' - Contacting Kimono %s with offset %s' % (url, offset))
    key = os.environ.get('KIMONO_API_KEY')
    fp = urllib.urlopen(url + '?apikey=' + key + '&kimoffset=%i' % (offset))
    results = json.load(fp)
    collection1 = results['results']['collection1']
    if results['count'] == 2500:
        new_collection1 = _get_results_collection1(url, offset=offset + 2500)
        collection1.extend(new_collection1)
    return collection1


def _fix_zero(value):
    '''
    Replaces the character '-' with the '0'
    '''
    # Match the '-' which are not followed by a number
    regex = '-(?![0-9])'
    return re.sub(regex, '0', value)


def _fix_role(value):
    '''
    Converting 'T (C)' or 'T (A)' to 'A' or 'C'. If there is no PDCA, it return
    the same value
    '''
    result = re.sub('[^PDCA]', '', value)
    return value if not result else result


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
