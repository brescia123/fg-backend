from models import Player, Vote


def populate_players(players_json):
    '''
    Used to populate the Player table with the json retrieved from Kimono
    '''
    players = players_json['results']['collection1']
    for player in players:
        p = Player()
        # TODO: remove dash and polish role:
        # 0 if player['price'] == '-' else player['price']
        # Using the last token of the URL as the pimary key
        p.key = player['name']['href'].split('/')[-1]
        p.name = player['name']['text']
        p.role = player['role']
        p.team = player['team']
        p.price = player['price']
        p.attendances = player['attendances']
        p.gol = player['gol']
        p.assist = player['assist']
        p.yellow_cards = player['yellow_cards']
        p.red_cards = player['red_cards']
        p.penalties_kicked = player['penalties_kicked']
        p.penalties_missed = player['penalties_missed']
        p.penalties_saved = player['penalties_saved']
        p.vote_avg = player['vote_avg']
        p.magicvote_avg = player['magicvote_avg']
        # Storing on the db
        p.save()
