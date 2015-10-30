from models import Player, Vote, Team
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fantagenius.api.serializers import TeamSerializer
from fantagenius.api import db_manager


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer


@api_view(['GET'])
def update_db(request):
    db_manager.update()
    return Response(status=status.HTTP_200_OK)
