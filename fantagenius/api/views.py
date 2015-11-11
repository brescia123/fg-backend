from models import Player, Vote, Team
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from fantagenius.api.serializers import TeamSerializer, PlayerSerializer
from fantagenius.api.serializers import VoteSerializer
from fantagenius.api import db_manager
from threading import Thread
import logging

logger = logging.getLogger(__name__)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Player.objects.all().order_by('name')
    serializer_class = PlayerSerializer


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vote.objects.all().order_by('day')
    serializer_class = VoteSerializer


@api_view(['POST'])
def update_db(request):
    if request.method == 'POST':
        logger.info('Update request')
        try:
            Thread(target=db_manager.update).start()
            return Response(data='Update started', status=status.HTTP_200_OK)
        except Exception, errtxt:
            logger.error(errtxt)
            return Response(data=errtxt,
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
