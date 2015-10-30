from django.conf.urls import include, url
from rest_framework import routers
from fantagenius.api import views

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
