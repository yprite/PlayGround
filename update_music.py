#!/usr/bin/python
#-*- coding: utf-8 -*-

# Todo List.!!
# code 변수 규칙 맞추기!!


import sys,time,random
import urllib
import BeautifulSoup


typing_speed =500 #wpm



def slow_type(t):
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*10.0/typing_speed)
    print ''


reload(sys)
sys.setdefaultencoding('utf-8')

song_title_list = {}



html = urllib.urlopen("http://www.mnet.com/chart/TOP100/")
mnetHtml = BeautifulSoup.BeautifulSoup(html)
topList = mnetHtml.find('table').findAll('a', {'class':'MMLI_Song'})

idx = 1
for title in topList:
	print title.text
	song_title_list[title.text]= idx
	idx = idx + 1 

# 순환하면서 찾아야 하는 로직 추가!

search_query ="https://www.youtube.com/results?search_query="+song_title_list.keys()[0].decode('utf-8').encode('utf-8')
print search_query
search_song_page = urllib.urlopen(search_query)
search_result_page = BeautifulSoup.BeautifulSoup(search_song_page)

#검색 후 하나 선택 해야됨 -> 인공지능 적용 ( 가중치 : 조회수, OFFICIAL 이라는 단어, ....)

search_result_page_titles = search_result_page.findAll('div', {'class':'yt-lockup-content'})
search_result_page_meta = search_result_page.findAll('div', {'class':'yt-lockup-meta'})

print "---------------------------------------------"
for title,meta in zip(search_result_page_titles,search_result_page_meta):
	print title.find('a')['title']
	print meta.find('ul').findAll('li')[1].text
	print ""


print slow_type(str(search_result_page))

'''
if __name__ == "__main__":
    try:
        main()
'''
