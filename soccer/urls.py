"""playground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin

from rest_framework import routers

from . import views
from . import rest_views

admin_router = routers.DefaultRouter()
admin_router.register(r'leagues', rest_views.LeaguesViewSet)
admin_router.register(r'levels', rest_views.LevelsViewSet)
admin_router.register(r'matchs', rest_views.MatchsViewSet)
admin_router.register(r'member_ability', rest_views.MemberAbilityViewSet)
admin_router.register(r'member_history', rest_views.MemberHistoryViewSet)
admin_router.register(r'members', rest_views.MembersViewSet)
admin_router.register(r'nations', rest_views.NationsViewSet)
admin_router.register(r'positions', rest_views.PositionsViewSet)
admin_router.register(r'roles', rest_views.RolesViewset)
admin_router.register(r'stadiums', rest_views.StadiumsViewset)
admin_router.register(r'teams', rest_views.TeamsViewset)
admin_router.register(r'users', rest_views.UsersViewset)
admin_router.register(r'predict', rest_views.MatchPredictVariableViewSet)
admin_router.register(r'weight', rest_views.WeightViewSet) #TODO: Change view class name

urlpatterns = [
        ##WEB VIEW
        url(r'^$', views.HomePageView.as_view(), name='home'),
        url(r'^index/', views.IndexPageView.as_view(), name='index'),

        ##REST VIEW
        url(r'^admin/', include(admin_router.urls), name='admin'),
        url(r'^v1/teams/name/(?P<team_name>.*)/$', rest_views.TeamViewSetByName.as_view(),
            name='v1_teams_name'),
        url(r'^v1/matchs/code/(?P<code>.*)/$', rest_views.MatchViewSetByCode.as_view(),
            name='v1_matchs_code'),
]
