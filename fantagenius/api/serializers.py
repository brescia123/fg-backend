from models import Player, Vote, Team
from rest_framework import serializers


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('url', 'name')
