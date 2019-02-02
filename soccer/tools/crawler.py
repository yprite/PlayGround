#https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/

import datetime
import requests
import json
from bs4 import BeautifulSoup

FILE_PATH = '/home/yprite/playground/soccer/tools/match_records/'

now = datetime.datetime.now()
now_date = now.strftime('%Y_%m_%d_%H_%M')

f = open(FILE_PATH + now_date, 'w')

s = requests.Session()
#req = requests.get('https://mobile.livescore.co.kr')
req = s.get('https://livescore.co.kr/developer/?process=score_board&what_phone=android&sports=soccer&date=&reg_id=&data=')

html = req.text

soup = BeautifulSoup(html, 'html.parser')

_list = json.loads(str(soup))
for item in _list:
	f.write(str(item))
f.close()
exit(1)

for item in _list:
    code= item['code']
    seq = item['seq']
    detail_url = 'https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore' + code + '&seq=' + seq
    #https://mobile.livescore.co.kr/sports/score_record/view.php?sports=soccer&code=livescore11531085&seq=8844650

    detail_soup = BeautifulSoup(s.get(detail_url).text, 'html.parser')
    divs = detail_soup.find_all('div', 'score_tbl_st1')
    print (type(divs))
    for div in divs:
        print (div)
        print ("-"*100)
    exit(1)
