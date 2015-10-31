from models import Player, Vote, Team
from rest_framework import serializers


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('url', 'name')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
