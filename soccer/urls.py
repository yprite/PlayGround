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

admin_router = routers.DefaultRouter()
admin_router.register(r'leagues', views.LeaguesViewSet)
admin_router.register(r'levels', views.LevelsViewSet)
admin_router.register(r'matchs', views.MatchsViewSet)
admin_router.register(r'member_ability', views.MemberAbilityViewSet)
admin_router.register(r'member_history', views.MemberHistoryViewSet)
admin_router.register(r'members', views.MembersViewSet)
admin_router.register(r'nations', views.NationsViewSet)
admin_router.register(r'positions', views.PositionsViewSet)
admin_router.register(r'roles', views.RolesViewset)
admin_router.register(r'stadiums', views.StadiumsViewset)
admin_router.register(r'teams', views.TeamsViewset)
admin_router.register(r'users', views.UsersViewset)

urlpatterns = [
        url(r'^admin/', include(admin_router.urls), name='admin'),
]
