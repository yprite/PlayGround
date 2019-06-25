#https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/

from bs4 import BeautifulSoup
import collections
import datetime
import io
import json
import logging
import pycurl
import requests


FILE_PATH = '/home/yprite/playground/soccer/tools/match_records/'

logger = logging.getLogger(__name__)

def get_past_record(session, detail_url):
    detail_soup = BeautifulSoup(session.get(detail_url).text, 'html.parser')
    divs = detail_soup.find_all('div', 'score_tbl_st1')
    if not divs is None:
        #varialbe
        history_total = 0
        history_win = 0
        history_draw = 0
        history_loss = 0
        
        home_recent_win = 0
        home_recent_draw = 0
        home_recent_loss = 0
        
        away_recent_win = 0
        away_recent_draw = 0
        away_recent_loss = 0
        for i, div in enumerate(divs):
            # Index Info
            # 0: 상대전적 
            # 1: 홈팀분석 
            # 2: 어웨이팀분

            if len(divs) != 3:
                return ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
            if i == 0:
                for index, child in enumerate(div.find('p').children):
                    #Indxe Info - 0: 상대전적
                    #0: Total 
                    #1: Win Count
                    #4: Draw Count
                    #5: Loss Count
                    if index == 0:
                        history_total = int(str(child).split(',')[0].split('총')[1].split('경기')[0].strip())
                    elif index == 1:
                        history_win = int(child.string)
                    elif index == 4:
                        history_draw = int(str(child).split(',')[1].split('무')[0].strip())
                    elif index == 5:
                        history_loss = int(child.string)
            elif i == 1:
                home_recent_win = len(div.find_all(string='승'))
                home_recent_draw = len(div.find_all(string='무'))
                home_recent_loss = len(div.find_all(string='패'))
            elif i == 2:
                away_recent_win = len(div.find_all(string='승'))
                away_recent_draw = len(div.find_all(string='무'))
                away_recent_loss = len(div.find_all(string='패'))
            else:
                print("Not support")

        return ((history_total, history_win, history_draw, history_loss, home_recent_win,
                home_recent_draw, home_recent_loss, away_recent_win, away_recent_draw,
                away_recent_loss))
    return ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0))


#DB Structure
# seq
# code
# league
# date
# stadium
# home
# away
# odds_home
# odds_draw
# odds_away
# history_total
# history_win
# history_draw
# history_loss
# home_recent_win
# home_recent_draw
# home_recent_loss
# away_recent_win
# away_recent_draw
# away_recent_loss
# home_team
# away_team
# home_coach
# away_coach
# home_x1 = 1 - odds_home (odds_home + odds_away)
# home_x2 = home_recent_win (home_recent_win + away_recent_win)
# home_x3 = history_win (history_win + history_loss)
#'leagueName': 'ENG PR', 
#'time': '23:05', 
#'Qtime': '', 
#'away_imageName': '/sports/images/logo/SOCCER///5985.png', 
#'premium_view': 'Y', 
#'home_name': '레스터 시티 FC', 
#'a_s_t': '0', 
#'code': '11240361', 
#'news': '', 
#'away_name': '맨체스터 유나이티드', 
#'a_rank': '6', 
#'seq': '8850352', 
#'h_s_t': '0', 
#'alarm': False, 
#'odds': None, 
#'states': 'PREP', 
#'type': '22', 
#'home_imageName': '/sports/images/logo/SOCCER///5770.png', 
#'statesCode': None, 
#'h_rank': '11'

MATCHINFO = collections.OrderedDict()
MATCHINFO['home_team']=''
MATCHINFO['away_team']=''
MATCHINFO['leagueName']=''
MATCHINFO['time']=''
MATCHINFO['code']=''
MATCHINFO['seq']=''
MATCHINFO['h_score']=''
MATCHINFO['a_score']=''
MATCHINFO['h_rank']=''
MATCHINFO['a_rank']=''
MATCHINFO['odds_home']=''
MATCHINFO['odds_draw']=''
MATCHINFO['odds_away']=''
MATCHINFO['history_total']=''
MATCHINFO['history_win']=''
MATCHINFO['history_draw']=''
MATCHINFO['history_loss']=''
MATCHINFO['home_recent_win']=''
MATCHINFO['home_recent_draw']=''
MATCHINFO['home_recent_loss']=''
MATCHINFO['away_recent_win']='' 
MATCHINFO['away_recent_draw']=''
MATCHINFO['away_recent_loss']=''

def is_filter_league(league):
    ok = ['ENG PR',  'JPN D1', 'ITA D1', 'KOR D1', 'SPA D1', 'GER D1']
    if league in ok:
        return True
    return False

def get_matchs_since_now():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    next = now + datetime.timedelta(days=1)

    #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
    url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
    req = session.get(url)

    logger.info('url : ' + url)

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    matchs = json.loads(str(soup))
    for i, item in enumerate(matchs):
        if is_filter_league(item['leagueName']) == False:
            continue
        home_team = item['home_name']
        away_team = item['away_name']
        time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
        code= item['code']
        seq = item['seq']
        odds_home = 0
        odds_draw = 0
        odds_away = 0

        if not item['odds'] is None:
            odds_home = item['odds']['current']['home']
            odds_draw = item['odds']['current']['draw']
            odds_away = item['odds']['current']['away']
        detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq

        #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
        #t2 = get_past_record(session, detail_url)
        d = MATCHINFO.copy()
        d['home_team']= str(home_team)
        d['away_team']= str(away_team)
        d['time']= time
        d['code']= str(code)
        d['seq']= str(seq)
        d['leagueName'] = str(item['leagueName'])
        d['odds_home']= str(odds_home)
        d['odds_draw']= str(odds_draw)
        d['odds_away']= str(odds_away)
        t  = get_past_record(session, detail_url)
        d['history_total']= str(t[0])
        d['history_win']= str(t[1])
        d['history_draw']= str(t[2])
        d['history_loss']= str(t[3])
        d['home_recent_win']= str(t[4])
        d['home_recent_draw']= str(t[5])
        d['home_recent_loss']= str(t[6])
        d['away_recent_win']= str(t[7])
        d['away_recent_draw']= str(t[8])
        d['away_recent_loss']= str(t[9])
        records.append(d)
    session.close()
    return records

def set_init_data_2018_2019_EPL():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(365, 0, -1):
        next = now - datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        
        matchs = json.loads(str(soup))
        for i, item in enumerate(matchs):
            if item['leagueName'] != 'ENG PR':
                continue
            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records
'''
U16
U17
U18
U20
U21
U23
WU-16
'''
def set_init_data_2012_2013_2014_2015_2016_2017_2018_2019_NATIONAL():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(1085, 365, -1):
        next = now - datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        
        matchs = json.loads(str(soup))
        for i, item in enumerate(matchs):
            is_pass = False
            if item['leagueName'] != 'INTERF':
                continue
            for generation in ['U15', 'U16', 'U17', 'U18', 'U19', 'U20', 'U21', 'U22', 'U23',
                    'WU-15', 'WU-16', 'WU-17, WU-18', 'WU-19', 'WU-20', 'WU-21', 'WU-22', 'WU-23', 'W',
                    '비치사커', '실내', '(N)']:
                if generation in item['home_name'] or generation in item['away_name']:
                    is_pass = True
                    break

            if is_pass == True:
                continue
            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            home_score = str(item['h_s_t'])
            away_score = str(item['a_s_t'])
            if item['h_rank'] == '':
                home_rank = 0
            else:
                home_rank = str(item['h_rank'])
            if item['a_rank'] == '':
                away_rank = 0
            else:
                away_rank = str(item['a_rank'])

            logger.info(" %s vs %s" % (home_team, away_team))
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['h_score'] = home_score
            d['a_score'] = away_score
            d['h_rank'] = home_rank
            d['a_rank'] = away_rank
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records

def get_match_result():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    prev = now - datetime.timedelta(days=1)

    url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
    req = session.get(url)

    logger.info('url : ' + url)

    html = req.text

    soup = BeautifulSoup(html, 'html.parser')

    matchs = json.loads(str(soup))
    for i, item in enumerate(matchs):
        if is_filter_league(item['leagueName']) == False:
            continue
        d = MATCHINFO.copy()
        d['home_team'] = str(item['home_name'])
        d['away_team'] = str(item['away_name'])
        d['code'] = str(item['code'])
        d['seq'] = str(item['seq'])
        d['h_score'] = str(item['h_s_t'])
        d['a_score'] = str(item['a_s_t'])
        d['h_rank'] = str(item['h_rank'])
        d['a_rank'] = str(item['a_rank'])
        records.append(d)
    session.close()
    return records

        
def get_data():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(0, 5, 1):
        next = now + datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            matchs = json.loads(str(soup))
        except Exception as E:
            print ('\r -> Error')
            continue

        if matchs is None:
            continue

        for i, item in enumerate(matchs):
            is_get = False
            is_pass = False

            #if t['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            if item['leagueName'] in ['KOR D1']:
            #if item['leagueName'] in ['INTERF']:
                is_get = True

            if is_get == False:
                continue
            if item['home_name'] is None or item['away_name'] is None:
                continue


            for generation in ['U15', 'U16', 'U17', 'U18', 'U19', 'U20', 'U21', 'U22', 'U23',
                    'WU-15', 'WU-16', 'WU-17, WU-18', 'WU-19', 'WU-20', 'WU-21', 'WU-22', 'WU-23', 'W',
                    '비치사커', '실내', '(N)']:
                if generation in item['home_name'] or generation in item['away_name']:
                    is_pass = True
                    break

            if is_pass == True:
                continue

            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            home_score = str(item['h_s_t'])
            away_score = str(item['a_s_t'])
            if item['h_rank'] == '':
                home_rank = 0
            else:
                home_rank = str(item['h_rank'])
            if item['a_rank'] == '':
                away_rank = 0
            else:
                away_rank = str(item['a_rank'])

            logger.info("%s vs %s" % (home_team, away_team))
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['h_score'] = home_score
            d['a_score'] = away_score
            d['h_rank'] = home_rank
            d['a_rank'] = away_rank
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records

def get_data2():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(0, 1, 1):
        next = now + datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            matchs = json.loads(str(soup))
        except Exception as E:
            print ('\r -> Error')
            continue

        if matchs is None:
            continue

        for i, item in enumerate(matchs):
            is_get = False
            is_pass = False

            if item['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            #if item['leagueName'] in ['KOR D1']:
            #if item['leagueName'] in ['INTERF']:
                is_get = True

            if is_get == False:
                continue
            if item['home_name'] is None or item['away_name'] is None:
                continue


            for generation in ['U15', 'U16', 'U17', 'U18', 'U19', 'U20', 'U21', 'U22', 'U23',
                    'WU-15', 'WU-16', 'WU-17, WU-18', 'WU-19', 'WU-20', 'WU-21', 'WU-22', 'WU-23', 'W',
                    '비치사커', '실내', '(N)']:
                if generation in item['home_name'] or generation in item['away_name']:
                    is_pass = True
                    break

            if is_pass == True:
                continue

            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            home_score = str(item['h_s_t'])
            away_score = str(item['a_s_t'])
            if item['h_rank'] == '':
                home_rank = 0
            else:
                home_rank = str(item['h_rank'])
            if item['a_rank'] == '':
                away_rank = 0
            else:
                away_rank = str(item['a_rank'])

            logger.info("%s vs %s" % (home_team, away_team))
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['h_score'] = home_score
            d['a_score'] = away_score
            d['h_rank'] = home_rank
            d['a_rank'] = away_rank
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records

def before_day_get_data():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(2, 0, -1):
        next = now - datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            matchs = json.loads(str(soup))
        except Exception as E:
            print ('\r -> Error')
            continue

        if matchs is None:
            continue

        for i, item in enumerate(matchs):
            is_get = False
            is_pass = False

            if item['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            #if item['leagueName'] in ['KOR D1']:
            #if item['leagueName'] in ['INTERF']:
                is_get = True

            if is_get == False:
                continue
            if item['home_name'] is None or item['away_name'] is None:
                continue


            for generation in ['U15', 'U16', 'U17', 'U18', 'U19', 'U20', 'U21', 'U22', 'U23',
                    'WU-15', 'WU-16', 'WU-17, WU-18', 'WU-19', 'WU-20', 'WU-21', 'WU-22', 'WU-23', 'W',
                    '비치사커', '실내', '(N)']:
                if generation in item['home_name'] or generation in item['away_name']:
                    is_pass = True
                    break

            if is_pass == True:
                continue

            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            home_score = str(item['h_s_t'])
            away_score = str(item['a_s_t'])
            if item['h_rank'] == '':
                home_rank = 0
            else:
                home_rank = str(item['h_rank'])
            if item['a_rank'] == '':
                away_rank = 0
            else:
                away_rank = str(item['a_rank'])

            logger.info("%s vs %s" % (home_team, away_team))
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['h_score'] = home_score
            d['a_score'] = away_score
            d['h_rank'] = home_rank
            d['a_rank'] = away_rank
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records

def next_day_get_data():
    records = []
    session = requests.Session()

    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')
    for day in range(0, 2, 1):
        next = now + datetime.timedelta(days=day)

        #url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data='
        url  = 'https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=' + next.strftime('%Y-%m-%d') + '&reg_id=&data='
        req = session.get(url)
        
        logger.info('url : ' + url)
        
        html = req.text
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            matchs = json.loads(str(soup))
        except Exception as E:
            print ('\r -> Error')
            continue

        if matchs is None:
            continue

        for i, item in enumerate(matchs):
            is_get = False
            is_pass = False

            if item['leagueName'] in ['INTERF', 'ENG_PR', 'KOR D1']:
            #if item['leagueName'] in ['KOR D1']:
            #if item['leagueName'] in ['INTERF']:
                is_get = True

            if is_get == False:
                continue
            if item['home_name'] is None or item['away_name'] is None:
                continue


            for generation in ['U15', 'U16', 'U17', 'U18', 'U19', 'U20', 'U21', 'U22', 'U23',
                    'WU-15', 'WU-16', 'WU-17, WU-18', 'WU-19', 'WU-20', 'WU-21', 'WU-22', 'WU-23', 'W',
                    '비치사커', '실내', '(N)']:
                if generation in item['home_name'] or generation in item['away_name']:
                    is_pass = True
                    break

            if is_pass == True:
                continue

            home_team = item['home_name']
            away_team = item['away_name']
            time = next.strftime('%Y-%m-%d') + ' ' + item['time'] + ':00'
            code= item['code']
            seq = item['seq']
            odds_home = 0
            odds_draw = 0
            odds_away = 0
            home_score = str(item['h_s_t'])
            away_score = str(item['a_s_t'])
            if item['h_rank'] == '':
                home_rank = 0
            else:
                home_rank = str(item['h_rank'])
            if item['a_rank'] == '':
                away_rank = 0
            else:
                away_rank = str(item['a_rank'])

            logger.info("%s vs %s" % (home_team, away_team))
            
            if not item['odds'] is None:
                odds_home = item['odds']['current']['home']
                odds_draw = item['odds']['current']['draw']
                odds_away = item['odds']['current']['away']
            
            detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
            logger.info('detail : ' + detail_url)

            #t1 = (home_team, away_team, time, code, seq, home_odd, draw_odd, away_odd)
            #t2 = get_past_record(session, detail_url)
            d = MATCHINFO.copy()
            d['home_team']= str(home_team)
            d['away_team']= str(away_team)
            d['time']= time
            d['code']= str(code)
            d['seq']= str(seq)
            d['leagueName'] = str(item['leagueName'])
            d['h_score'] = home_score
            d['a_score'] = away_score
            d['h_rank'] = home_rank
            d['a_rank'] = away_rank
            d['odds_home']= str(odds_home)
            d['odds_draw']= str(odds_draw)
            d['odds_away']= str(odds_away)
            t  = get_past_record(session, detail_url)
            d['history_total']= str(t[0])
            d['history_win']= str(t[1])
            d['history_draw']= str(t[2])
            d['history_loss']= str(t[3])
            d['home_recent_win']= str(t[4])
            d['home_recent_draw']= str(t[5])
            d['home_recent_loss']= str(t[6])
            d['away_recent_win']= str(t[7])
            d['away_recent_draw']= str(t[8])
            d['away_recent_loss']= str(t[9])
            records.append(d)
    session.close()
    return records
