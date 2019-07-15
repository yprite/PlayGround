#!/usr/bin/python
#-*- coding: utf-8 -*-

# TODO
# sudo apt-get install youtube-dl 

import re
import sys,time,random
import requests
import os
from bs4 import BeautifulSoup


music_chart_url = "http://www.mnet.com/chart/TOP100/"
download_folder = "download/"
downloaded_file_lists = "list.txt"
ong_title_list = []

def init():
    if not os.path.exists(download_folder):
        os.mkdir(download_folder)

    if not os.path.exists(downloaded_file_lists):
        f = open(downloaded_file_lists, 'w')
        f.close()
    else:
        f = open(downloaded_file_lists, 'r')
        for line in f.readlines():
            song_title_list.append(line)
        f.close()


def main():
    def downloader(url):
        try:
            url = "https://www.youtube.com/watch?v=" + url
            cmd = 'youtube-dl --extract-audio --audio-format mp3 -o ' + download_folder + '"%(title)s.%(ext)s" ' + url
            os.system(cmd)
        except Exception as E:
            print ("Error downaloading %s (%s) " % (url, E))
            return False
        return True

    session = requests.Session()
    mnetHtml = BeautifulSoup(session.get(music_chart_url).text, 'html.parser')
    topList = mnetHtml.find('table').findAll('a', {'class':'MMLI_Song'})
    
    for title in topList:
        if title.text in song_title_list:
            print ("%s pass" % (title.text))
        else:
            song_title_list.append(title.text)
            search_query = "https://www.youtube.com/results?search_query=" + title.text
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', session.get(search_query).text)
            #검색 후 하나 선택 해야됨 ->  가중치 : 조회수, OFFICIAL 이라는 단어, ....
            downloader(search_results[0])
            print ("%s donwloaded" % (title.text))

def finish(): 
    if os.path.exists(downloaded_file_lists):
        f = open(downloaded_file_lists, 'w')
        for line in song_title_list:
            f.write(line)
        f.close()


if __name__ == "__main__":
    #init()
    main()
    #finish()

