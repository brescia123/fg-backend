
from django.test import TestCase
from models import Player, Vote, Team
from django.conf import settings
import db_manager as dm


class DbManagerTest(TestCase):
    def test_fix_role(self):
        self.assertEqual(dm._fix_role('T( C )'), 'C')
        self.assertEqual(dm._fix_role('T( A )'), 'A')
        self.assertEqual(dm._fix_role('T( P )'), 'P')
        self.assertEqual(dm._fix_role('T( D )'), 'D')

    def test_fix_zero(self):
        self.assertEqual(dm._fix_zero('-'), '0')
        self.assertEqual(dm._fix_zero('-1'), '-1')
        self.assertEqual(dm._fix_zero('-10'), '-10')
        self.assertEqual(dm._fix_zero('1'), '1')

    def test_name_from_id(self):
        self.assertEqual(dm._name_from_id('giacomo_bresciani_777'),
                         'Giacomo Bresciani')
        self.assertEqual(dm._name_from_id('giacomo_bear_bresciani_777'),
                         'Giacomo Bear Bresciani')
        self.assertEqual(dm._name_from_id('giacomo_777'), 'Giacomo')

    def test_init_teams(self):
        url = settings.KIMONO['teams_url']
        teams = dm._get_results_collection1(url)
        dm.init_teams()
        no_db_teams = Team.objects.all().count()
        # Check if the teams in the db are the same and only the ones found by
        # Kimono
        self.assertEqual(len(teams), no_db_teams)
        for team in teams:
            team_queryset = Team.objects.filter(name=team['name'])
            self.assertEqual(len(team_queryset), 1)
            db_team = team_queryset[0]
            self.assertEqual(db_team.name, team['name'])

    def test_update_players(self):
        url = settings.KIMONO['players_url']
        players = dm._get_results_collection1(url)
        # Initializing teams. They are not stored from previous test.
        dm.init_teams()
        dm.update_players()
        no_db_players = Player.objects.all().count()
        # Check if the Player in the db are the same and only the ones found by
        # Kimono
        self.assertEqual(len(players), no_db_players)
        for player in players:
            p_id = dm._id_from_url(player['name']['href'])
            player_queryset = Player.objects.filter(pk=p_id)
            self.assertEqual(len(player_queryset), 1)
            db_p = player_queryset[0]
            self.assertEqual(db_p.name, player['name']['text'])
            self.assertEqual(db_p.role, dm._fix_role(player['role']))
            db_team = Team.objects.get(name__iexact=player['team'])
            self.assertEqual(db_p.team, db_team)
            self.assertEqual(db_p.price,
                             int(dm._fix_zero(player['price'])))
            self.assertEqual(db_p.attendances,
                             int(dm._fix_zero(player['attendances'])))
            self.assertEqual(db_p.gol,
                             int(dm._fix_zero(player['gol'])))
            self.assertEqual(db_p.assist,
                             int(dm._fix_zero(player['assist'])))
            self.assertEqual(db_p.yellow_cards,
                             int(dm._fix_zero(player['yellow_cards'])))
            self.assertEqual(db_p.red_cards,
                             int(dm._fix_zero(player['red_cards'])))
            self.assertEqual(db_p.penalties_kicked,
                             int(dm._fix_zero(player['penalties_kicked'])))
            self.assertEqual(db_p.penalties_scored,
                             int(dm._fix_zero(player['penalties_scored'])))
            self.assertEqual(db_p.penalties_saved,
                             int(dm._fix_zero(player['penalties_saved'])))
            self.assertEqual(db_p.vote_avg,
                             float(dm._fix_zero(player['vote_avg'])))
            self.assertEqual(db_p.magicvote_avg,
                             float(dm._fix_zero(player['magicvote_avg'])))
            # TODO check seriea
