import requests
from bs4 import BeautifulSoup

from nojapan import models


def get_korea_company_info():
    def clean_html_tag(raw_html):
        import re
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    session = requests.Session()
    url = "https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B8%B0%EC%97%85_%EB%AA%A9%EB%A1%9D"
    content = BeautifulSoup(session.get(url).text, 'html.parser')
    for element in content.find('div', id='mw-content-text').find('div', class_="mw-parser-output").find('ul').find_all('a') :
        print (element['href'])
        print (element.text)
        #product, is_created = models.product.objects.get_or_create(name=str(element.text))
        #print ("Save " + str(is_created))
        #print ("--------------------------------")
