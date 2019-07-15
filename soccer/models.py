from django.db import models

# Create your models here.

class Roles(models.Model):
   name = models.CharField(max_length=200) 
   privilege = models.CharField(max_length=200)
   def __str__(self):
       return self.name

class Levels(models.Model):
    #S:Real Madrid,Barcellona
    #A:AT Madrid,
    #B:Ajax
    #C:Chonbuk Hyundai
    #D:
    #E:
   name = models.CharField(max_length=200) 

   def __str__(self):
       return self.name

class Nations(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Users(models.Model):
    name = models.CharField(max_length=200)
    mail = models.CharField(max_length=200) #ACCOUNUT, SNS ACCOUNT
    nation = models.ForeignKey(Nations, on_delete=None)
    role = models.ForeignKey(Roles, on_delete=None)
    def __str__(self):
        return self.name

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
    def __str__(self):
        return self.name

class Members(models.Model):
    users = models.ForeignKey(Users, on_delete=None)
    age = models.CharField(max_length=200)
    position = models.ForeignKey(Positions, on_delete=None)
    nation = models.ForeignKey(Nations, on_delete=None)
    myteam = models.CharField(max_length=200)   #TODO:Need to decide one team or some teams
#    favteam = models.CharField(max_length=200)  #TODO:Fixed multiple selection.
    def __str__(self):
        return self.users.name

class Stadiums(models.Model):
    name = models.CharField(max_length=200)
    nation = models.ForeignKey(Nations, on_delete=None)
    city = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Leagues(models.Model):
    name = models.CharField(max_length=200)
    nation = models.ForeignKey(Nations, on_delete=None, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    level = models.ForeignKey(Levels, on_delete=None, null=True, blank=True)
    def __str__(self):
        return self.name

class Teams(models.Model):
    name = models.CharField(max_length=200)
    coach =  models.ForeignKey(Users, on_delete=None, null=True, blank=True)
    date =  models.DateField(auto_now_add=True)
    league = models.ForeignKey(Leagues, on_delete=None, null=True, blank=True)
    stadium = models.ForeignKey(Stadiums, on_delete=None, null=True, blank=True)
    mmr = models.IntegerField(null=True, blank=True) #match making rating
    fifaid = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.name

class Seasons(models.Model):
    team = models.ForeignKey(Teams, on_delete=None, null=True, blank=True)
    season = models.CharField(max_length=200, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    win = models.IntegerField(null=True, blank=True)
    draw = models.IntegerField(null=True, blank=True)
    defeat = models.IntegerField(null=True, blank=True)
    goal = models.IntegerField(null=True, blank=True)
    loss = models.IntegerField(null=True, blank=True)
    assist  = models.IntegerField(null=True, blank=True)
    foul = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.team.name

class Matchs(models.Model):
    seq = models.CharField(max_length=200, null=True)
    code = models.CharField(max_length=200, null=True)
    league = models.ForeignKey(Leagues, on_delete=None, null=True, blank=True)
    date =  models.CharField(max_length=200, null=True)
    #date =  models.DateTimeField(null=True)
    stadium = models.ForeignKey(Stadiums, on_delete=None, null=True, blank=True)
    home =  models.ForeignKey(Teams, on_delete=None, related_name="home", null=True, blank=True) #TODO:Change not null
    away =  models.ForeignKey(Teams, on_delete=None, related_name="away", null=True, blank=True) #TODO:Change not null
    #TODO:Insert state field (0:NOT YET, 1:ING, 2:END) 
    hscore = models.IntegerField(null=True, blank=True)
    ascore = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return '%s vs %s' % (self.home, self.away)

class MatchPredictVariables(models.Model):
    match = models.ForeignKey(Matchs, on_delete=None)
    h_x1 = models.FloatField(null=True, blank=True, default=None)
    h_x2 = models.FloatField(null=True, blank=True, default=None)
    h_x3 = models.FloatField(null=True, blank=True, default=None)
    h_x4 = models.FloatField(null=True, blank=True, default=None)
    h_x5 = models.FloatField(null=True, blank=True, default=None)
    h_x6 = models.FloatField(null=True, blank=True, default=None)
    a_x1 = models.FloatField(null=True, blank=True, default=None)
    a_x2 = models.FloatField(null=True, blank=True, default=None)
    a_x3 = models.FloatField(null=True, blank=True, default=None)
    a_x4 = models.FloatField(null=True, blank=True, default=None)
    a_x5 = models.FloatField(null=True, blank=True, default=None)
    a_x6 = models.FloatField(null=True, blank=True, default=None)
    def __str__(self):
        return str(self.match)

class Weigth(models.Model): #TODO: Fix name.
    w1 = models.FloatField(null=True, blank=True, default=None)
    w2 = models.FloatField(null=True, blank=True, default=None)
    w3 = models.FloatField(null=True, blank=True, default=None)
    w4 = models.FloatField(null=True, blank=True, default=None)
    w5 = models.FloatField(null=True, blank=True, default=None)
    w6 = models.FloatField(null=True, blank=True, default=None)


class MemberAbility(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

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

class FreeBoard(models.Model):
    subject = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True)
    created_date = models.DateField(null=True, blank=True)
    mail = models.CharField(max_length=50, blank=True)
    memo = models.CharField(max_length=200, blank=True)
    hits = models.IntegerField(null=True, blank=True) 
