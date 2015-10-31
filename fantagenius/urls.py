from django.conf.urls import include, url
from rest_framework import routers
from fantagenius.api import views

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'player', views.PlayerViewSet)
router.register(r'vote', views.VoteViewSet)

urlpatterns = [
    url(r'update', views.update_db),
    url(r'^', include(router.urls)),
]
