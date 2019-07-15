from django.contrib import admin

from .models import Roles, Levels
from .models import Nations, Users, Positions, Members, Stadiums, Leagues, Teams, Matchs, Seasons
from .models import MatchPredictVariables, Weigth, MemberAbility, MemberHistory



# Register your models here.

admin.site.register(Roles)
admin.site.register(Levels)
admin.site.register(Nations)
admin.site.register(Users)
admin.site.register(Positions)
admin.site.register(Members)
admin.site.register(Stadiums)
admin.site.register(Leagues)
admin.site.register(Teams)
admin.site.register(Matchs)
admin.site.register(MatchPredictVariables)
admin.site.register(Weigth)
admin.site.register(MemberAbility)
admin.site.register(Seasons)

