from rest_framework import serializers

from . import models

class LeaguesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Leagues
        fields = '__all__'
class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Levels
        fields = '__all__'
class MatchsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Matchs
        fields = '__all__'
class MemberAbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemberAbility
        fields = '__all__'
class MemberHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MemberHistory
        fields = '__all__'
class MembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Members
        fields = '__all__'
class NationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nations
        fields = '__all__'
class PositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Positions
        fields = '__all__'
class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Roles
        fields = '__all__'
class StadiumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stadiums
        fields = '__all__'
class TeamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Teams
        fields = '__all__'
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Users
        fields = '__all__'
