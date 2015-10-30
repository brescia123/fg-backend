from models import Player, Vote, Team
from rest_framework import viewsets
from fantagenius.api.serializers import TeamSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer
