from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from . import models
from . import serializers
# Create your views here.

class LeaguesViewSet(viewsets.ModelViewSet):
    queryset = models.Leagues.objects.all()
    serializer_class = serializers.LeaguesSerializer
    #permission_classes = [permissions.IsAdminUser]#TODO:It should be added

class LevelsViewSet(viewsets.ModelViewSet):
    queryset = models.Levels.objects.all()
    serializer_class = serializers.LevelsSerializer

class MatchsViewSet(viewsets.ModelViewSet):
    queryset = models.Matchs.objects.all()
    serializer_class = serializers.MatchsSerializer

class MemberAbilityViewSet(viewsets.ModelViewSet):
    queryset = models.MemberAbility.objects.all()
    serializer_class = serializers.MemberAbilitySerializer

class MemberHistoryViewSet(viewsets.ModelViewSet):
    queryset = models.MemberHistory.objects.all()
    serializer_class = serializers.MemberHistorySerializer

class MembersViewSet(viewsets.ModelViewSet):
    queryset = models.Members.objects.all()
    serializer_class = serializers.MembersSerializer

class NationsViewSet(viewsets.ModelViewSet):
    queryset = models.Nations.objects.all()
    serializer_class = serializers.NationsSerializer

class PositionsViewSet(viewsets.ModelViewSet):
    queryset = models.Positions.objects.all()
    serializer_class = serializers.PositionsSerializer

class RolesViewset(viewsets.ModelViewSet):
    queryset = models.Roles.objects.all()
    serializer_class = serializers.RolesSerializer

class StadiumsViewset(viewsets.ModelViewSet):
    queryset = models.Stadiums.objects.all()
    serializer_class = serializers.StadiumsSerializer

class TeamsViewset(viewsets.ModelViewSet):
    queryset = models.Teams.objects.all()
    serializer_class = serializers.TeamsSerializer

class UsersViewset(viewsets.ModelViewSet):
    queryset = models.Users.objects.all()
    serializer_class = serializers.UsersSerializer

