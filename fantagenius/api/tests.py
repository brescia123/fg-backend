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
            self.assertEqual(len(Team.objects.filter(name=team['name'])), 1)
