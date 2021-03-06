import gc
import logging
import datetime
import tracemalloc

from .tools import dev_crawler
from . import models

from django.db.models import Q

logger = logging.getLogger(__name__)

def my_cron_job():
    now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info("[%s]Test Debug Mesasge", now_date)
    #dev_crawler.get_match_info()

def set_future_match_data():
    #Index Info
    # 0     : home_team
    # 1     : away_team
    # 2     : time
    # 3     : code
    # 4     : seq
    # 5     : odds_home
    # 6     : odds_draw
    # 7     : odds_away
    # 8     : history_total
    # 9     : history_win
    # 10    : history_draw
    # 11    : history_loss
    # 12    : home_recent_win
    # 13    : home_recent_draw
    # 14    : home_recent_loss
    # 15    : away_recent_win
    # 16    : away_recent_draw
    # 17    : away_recent_loss

    ts = dev_crawler.get_matchs_since_now()
    #ts = dev_crawler.set_init_data_2018_2019_EPL()
    logger.info("get_matchs_since_now() size= %d [SUCCESS]", len(ts))
    for t in ts:
        logger.info(t)
        if t['leagueName'] != 'ENG PR':
            logger.info('%s -> pass', t['leagueName'])
            continue
        
        league, league_is_created = models.Leagues.objects.get_or_create(name=t['leagueName'])
        logger.info("%s [PASS]", league.name)

        h_team, h_team_is_craeted = models.Teams.objects.get_or_create(name=t['home_team'])
        if h_team_is_craeted:
            h_team.league = league
            h_team.save()
            logger.info("%s get_or_create [SUCCSS]", h_team.name)
            
        a_team, a_team_is_created = models.Teams.objects.get_or_create(name=t['away_team'])
        if a_team_is_created:
            a_team.league = league
            a_team.save()
            logger.info("%s get_or_create [SUCCSS]", a_team.name)
    
        match, match_is_created = models.Matchs.objects.get_or_create(code=t['code'])
        if match_is_created:
            logger.info("%s get_or_create [SUCCSS]", match.code)
            match.seq = t['seq']
            match.date = t['time']
            match.home = h_team
            match.away = a_team
            match.save()
            logger.info("%s (%s vs %s) save [SUCCSS]", match.code, match.home, match.away)
        else:
            logger.info("%s (%s vs %s) [PASS]", match.code, match.home, match.away)

        


        match_predict_variable, mpv_is_created = models.MatchPredictVariables.objects.get_or_create(match=match)
        if mpv_is_created:
            logger.info("%s get_or_create [SUCCSS]", match_predict_variable.match)
            
        if float(t['odds_home']) + float(t['odds_away']) != 0:
            match_predict_variable.h_x1 = 1 - (float(t['odds_home']) / (float(t['odds_home']) + float(t['odds_away'])))
            match_predict_variable.a_x1 = 1 - (float(t['odds_away']) / (float(t['odds_home']) + float(t['odds_away'])))
        else:
            match_predict_variable.h_x1 = 0
            match_predict_variable.a_x1 = 0
            
        if int(t['home_recent_win']) + int(t['home_recent_loss']) != 0:
            match_predict_variable.h_x2 = float(t['home_recent_win']) / (float(t['home_recent_win']) + float(t['home_recent_loss']))
            match_predict_variable.a_x2 = float(t['home_recent_loss']) / (float(t['home_recent_win']) + float(t['home_recent_loss']))
        else:
            match_predict_variable.h_x2 =0
            match_predict_variable.a_x2 =0
            
        if int(t['history_win']) + int(t['history_loss']) != 0:
            match_predict_variable.h_x3 = float(t['history_win']) / (float(t['history_win']) + float(t['history_loss']))
            match_predict_variable.a_x3 = float(t['history_win']) / (float(t['history_win']) + float(t['history_loss']))
        else:
            match_predict_variable.h_x3 = 0
            match_predict_variable.a_x3 = 0
            
        if int(t['home_recent_draw']) + int(t['away_recent_draw']) != 0:
            match_predict_variable.h_x4 = float(t['home_recent_draw']) / (float(t['home_recent_draw']) + float(t['away_recent_draw']))
            match_predict_variable.a_x4 = float(t['away_recent_draw']) / (float(t['home_recent_draw']) + float(t['away_recent_draw']))
        else:
            match_predict_variable.h_x4 = 0
            match_predict_variable.a_x4 = 0

        match_predict_variable.save()
   
def set_result_match_data():
    ts = dev_crawler.get_match_result()
    logger.info("get_match_result() Done")
    exit(1)

    for t in ts:
        #Three conditions should check null.
        seq = ''
        code = ''
        h_team = ''
        a_team = ''

def func1():
    logger.info ("==================================================")
    logger.info ("YPRITE:BEGIN")
    update_before_day_match_data()
    update_next_day_match_data()
    update_team_rank()
    logger.info ("YPRITE:END")
    logger.info ("==================================================")

def func2():
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    next_date = now_date + datetime.timedelta(days=1)
    print (next_date)

def set_national_match_data():
    pass

def update_before_day_match_data():
    '''
    National, EPL, K-League
    '''
    #Index Info
    # 0     : home_team
    # 1     : away_team
    # 2     : time
    # 3     : code
    # 4     : seq
    # 5     : odds_home
    # 6     : odds_draw
    # 7     : odds_away
    # 8     : history_total
    # 9     : history_win
    # 10    : history_draw
    # 11    : history_loss
    # 12    : home_recent_win
    # 13    : home_recent_draw
    # 14    : home_recent_loss
    # 15    : away_recent_win
    # 16    : away_recent_draw
    # 17    : away_recent_loss

    #ts = dev_crawler.get_matchs_since_now()
    ts = dev_crawler.before_day_get_data()
    logger.info("before_day_get_data() size= %d [SUCCESS]", len(ts))
    for t in ts:
        is_get = False
        logger.info("DATA")
        logger.info(t)
        logger.info("---------------------------------------------------------------------")
        if t['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            is_get = True

        if is_get == False:
            continue
        
        league, league_is_created = models.Leagues.objects.get_or_create(name=t['leagueName'])
        logger.info("%s [GET SUCCESS]", league.name)

        h_team, h_team_is_craeted = models.Teams.objects.get_or_create(name=t['home_team'])
        if h_team_is_craeted:
            h_team.league = league
            h_team.save()
        else:
            h_team.save()
        logger.info("home team %s done [SUCCSS]", h_team.name)
            
        a_team, a_team_is_created = models.Teams.objects.get_or_create(name=t['away_team'])
        if a_team_is_created:
            a_team.league = league
            a_team.save()
        else:
            a_team.save()
        logger.info("away team %s done [SUCCSS]", a_team.name)
        
        if t['code'] is None:
            match, match_is_created = models.Matchs.objects.get_or_create(seq=t['seq'])
            if match_is_created:
                logger.info("seq[%s] match_is_created is True", match.seq)
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.hscore = t['h_score']
                match.ascore = t['a_score']
                match.save()
                logger.info("%s (%s vs %s) save [SUCCSS]", match.seq, match.home, match.away)
            else:
                logger.info("seq[%s] match_is_created is False", match.seq)
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.hscore = t['h_score']
                match.ascore = t['a_score']
                match.save()
                logger.info("%s (%s vs %s) update [SUCCESS]", match.seq, match.home, match.away)
        else:
            match, match_is_created = models.Matchs.objects.get_or_create(code=t['code'])
            if match_is_created:
                logger.info("%s match_is_created is True", match.code)
                match.seq = t['seq']
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.hscore = t['h_score']
                match.ascore = t['a_score']
                match.save()
                logger.info("%s (%s vs %s) save [SUCCSS]", match.code, match.home, match.away)
            else:
                logger.info("%s match_is_created is False", match.code)
                match.seq = t['seq']
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.hscore = t['h_score']
                match.ascore = t['a_score']
                match.save()
                logger.info("%s (%s vs %s) update [SUCCESS]", match.code, match.home, match.away)


def update_next_day_match_data():
    '''
    National, EPL, K-League
    '''
    #Index Info
    # 0     : home_team
    # 1     : away_team
    # 2     : time
    # 3     : code
    # 4     : seq
    # 5     : odds_home
    # 6     : odds_draw
    # 7     : odds_away
    # 8     : history_total
    # 9     : history_win
    # 10    : history_draw
    # 11    : history_loss
    # 12    : home_recent_win
    # 13    : home_recent_draw
    # 14    : home_recent_loss
    # 15    : away_recent_win
    # 16    : away_recent_draw
    # 17    : away_recent_loss

    #ts = dev_crawler.get_matchs_since_now()
    ts = dev_crawler.next_day_get_data()
    logger.info("next_day_get_data() size= %d [SUCCESS]", len(ts))
    for t in ts:
        is_get = False
        logger.info("DATA")
        logger.info(t)
        logger.info("---------------------------------------------------------------------")
        if t['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            is_get = True

        if is_get == False:
            continue
        
        league, league_is_created = models.Leagues.objects.get_or_create(name=t['leagueName'])
        logger.info("%s [GET SUCCESS]", league.name)

        h_team, h_team_is_craeted = models.Teams.objects.get_or_create(name=t['home_team'])
        if h_team_is_craeted:
            h_team.league = league
            h_team.save()
        logger.info("home team %s done [SUCCSS]", h_team.name)
            
        a_team, a_team_is_created = models.Teams.objects.get_or_create(name=t['away_team'])
        if a_team_is_created:
            a_team.league = league
            a_team.save()
        logger.info("away team %s done [SUCCSS]", a_team.name)
        
        if t['code'] is None:
            match, match_is_created = models.Matchs.objects.get_or_create(seq=t['seq'])
            if match_is_created:
                logger.info("seq[%s] match_is_created is True", match.seq)
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.save()
                logger.info("%s (%s vs %s) save [SUCCSS]", match.seq, match.home, match.away)
            else:
                logger.info("seq[%s] match_is_created is False", match.seq)
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.save()
                logger.info("%s (%s vs %s) update [SUCCESS]", match.seq, match.home, match.away)

        else:
            match, match_is_created = models.Matchs.objects.get_or_create(code=t['code'])
            if match_is_created:
                logger.info("%s match_is_created is True", match.code)
                match.seq = t['seq']
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.save()
                logger.info("%s (%s vs %s) save [SUCCSS]", match.code, match.home, match.away)
            else:
                logger.info("%s match_is_created is False", match.code)
                match.seq = t['seq']
                match.date = t['time']
                match.home = h_team
                match.away = a_team
                match.league = league
                match.save()
                logger.info("%s (%s vs %s) update [SUCCESS]", match.code, match.home, match.away)


        match_predict_variable, mpv_is_created = models.MatchPredictVariables.objects.get_or_create(match=match)
        if mpv_is_created:
            logger.info("%s get_or_create [SUCCSS]", match_predict_variable.match)
            
        if float(t['odds_home']) + float(t['odds_away']) != 0:
            match_predict_variable.h_x1 = 1 - (float(t['odds_home']) / (float(t['odds_home']) + float(t['odds_away'])))
            match_predict_variable.a_x1 = 1 - (float(t['odds_away']) / (float(t['odds_home']) + float(t['odds_away'])))
            
        if int(t['home_recent_win']) + int(t['home_recent_loss']) != 0:
            match_predict_variable.h_x2 = float(t['home_recent_win']) / (float(t['home_recent_win']) + float(t['home_recent_loss']))
            match_predict_variable.a_x2 = float(t['home_recent_loss']) / (float(t['home_recent_win']) + float(t['home_recent_loss']))
            
        if int(t['history_win']) + int(t['history_loss']) != 0:
            match_predict_variable.h_x3 = float(t['history_win']) / (float(t['history_win']) + float(t['history_loss']))
            match_predict_variable.a_x3 = float(t['history_win']) / (float(t['history_win']) + float(t['history_loss']))
            
        if int(t['home_recent_draw']) + int(t['away_recent_draw']) != 0:
            match_predict_variable.h_x4 = float(t['home_recent_draw']) / (float(t['home_recent_draw']) + float(t['away_recent_draw']))
            match_predict_variable.a_x4 = float(t['away_recent_draw']) / (float(t['home_recent_draw']) + float(t['away_recent_draw']))

        match_predict_variable.save()

def update_team_rank():
    '''
    K-League rank update
    '''
    k_league = models.Leagues.objects.get(name='KOR D1')
    for row in dev_crawler.get_k_league_rank():
        try:
            print (row[1])
            print ("--------------------------------------------")
            team = models.Teams.objects.get(name__contains=row[1], league=k_league)
            season, is_created = models.Seasons.objects.get_or_create(team=team)
            season.season = datetime.datetime.now().strftime('%Y-%m-%d')
            season.team = team
            season.rank = row[0]
            season.win = row[2]
            season.draw = row[3]
            season.defeat = row[4]
            season.goal = row[5]
            season.loss = row[6]
            season.assist = row[7]
            season.foult = row[8]
            season.save()
            print ("Update (%s %s %s %s %s %s %s %s)" % (row[0], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
            print ("--------------------------------------------")

        except Exception as E:
            print (E)

