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

MATCHINFO = collections.OrderedDict()
MATCHINFO['home_team']=''
MATCHINFO['away_team']=''
MATCHINFO['time']=''
MATCHINFO['code']=''
MATCHINFO['seq']=''
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
        #d['odds_home']= str(odds_home)
        #d['odds_draw']= str(odds_draw)
        #d['odds_away']= str(odds_away)
        #t  = get_past_record(session, detail_url)
        #d['history_total']= str(t[0])
        #d['history_win']= str(t[1])
        #d['history_draw']= str(t[2])
        #d['history_loss']= str(t[3])
        #d['home_recent_win']= str(t[4])
        #d['home_recent_draw']= str(t[5])
        #d['home_recent_loss']= str(t[6])
        #d['away_recent_win']= str(t[7])
        #d['away_recent_draw']= str(t[8])
        #d['away_recent_loss']= str(t[9])
        records.append(d)
    session.close()
    return records
