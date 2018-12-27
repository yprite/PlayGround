from django.db import models

# Create your models here.

class Roles(models.Model):
   name = models.CharField(max_length=200) 
   privilege = models.CharField(max_length=200)

class Levels(models.Model):
    #S:Real Madrid,Barcellona
    #A:AT Madrid,
    #B:Ajax
    #C:Chonbuk Hyundai
    #D:
    #E:
   name = models.CharField(max_length=200) 

class Nations(models.Model):
    name = models.CharField(max_length=200)

class Users(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200) #ACCOUNUT, SNS ACCOUNT
    nation = models.ForeignKey(Nations, on_delete=None)
    role = models.ForeignKey(Roles, on_delete=None)

class Positions(models.Model):
    GK = 0
    SW = 1
    RB = 20
    CB = 21
    LB = 22
    RWB = 30
    DM = 31
    LWB = 32
    RM = 33
    CM = 34
    LM = 35
    AM = 36
    RW = 40
    SS = 41
    LW = 42
    CF = 43

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Members(models.Model):
    users = models.ForeignKey(Users, on_delete=None)
    age = models.CharField(max_length=200)
    position = models.ForeignKey(Positions, on_delete=None)
    nation = models.ForeignKey(Nations, on_delete=None)
    myteam = models.CharField(max_length=200)   #TODO:Need to decide one team or some teams
#    favteam = models.CharField(max_length=200)  #TODO:Fixed multiple selection.

class Stadiums(models.Model):
    name = models.CharField(max_length=200)
    nation = models.ForeignKey(Nations, on_delete=None)
    city = models.CharField(max_length=200)

class Leagues(models.Model):
    name = models.CharField(max_length=200)
    nation = models.ForeignKey(Nations, on_delete=None)
    description = models.CharField(max_length=200)
    level = models.ForeignKey(Levels, on_delete=None)    

class Teams(models.Model):
    name = models.CharField(max_length=200)
    coach =  models.ForeignKey(Users, on_delete=None, null=True, blank=True)
    date =  models.DateField()
    league = models.ForeignKey(Leagues, on_delete=None, null=True, blank=True)
    stadium = models.ForeignKey(Stadiums, on_delete=None, null=True, blank=True)
    mmr = models.IntegerField() #match making rating

class Matchs(models.Model):
    league = models.ForeignKey(Leagues, on_delete=None)
    date =  models.DateTimeField()
    result =  models.CharField(max_length=200)
    home =  models.ForeignKey(Teams, on_delete=None, related_name="home")
    away =  models.ForeignKey(Teams, on_delete=None, related_name="away")
    scorer = models.ForeignKey(Members, on_delete=None)

class MemberAbility(models.Model):
    name = models.CharField(max_length=200)

class MemberHistory(models.Model):
    player = models.ForeignKey(Members, on_delete=None)
    team = models.ForeignKey(Teams, on_delete=None)
    match = models.ForeignKey(Matchs, on_delete=None)
    goal = models.IntegerField()
    assist = models.IntegerField()
    yellow = models.IntegerField()
    red = models.IntegerField()
    shoot = models.IntegerField()
    passs = models.IntegerField()
