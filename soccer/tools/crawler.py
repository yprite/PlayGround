#https://beomi.github.io/2017/01/20/HowToMakeWebCrawler-With-Login/


import requests
from bs4 import BeautifulSoup


req = requests.get('https://mobile.livescore.co.kr')

html = req.text

soup = BeautifulSoup(html, 'html.parser')

print (soup)
