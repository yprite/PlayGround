#TODO : Should be modifed or added
# 1) All of database struct modify the Collections.OrderedDict.
# 2) Mehthod is same like 1)
#

#Check things like below
# 1. Python Version
# 2. Argument : file at post
import os
import sys

import json
import pycurl
import collections

URLS = {
        'Leagues':'0.0.0.0:8080/playground/soccer/admin/leagues/',
        'Levels':'0.0.0.0:8080/playground/soccer/admin/levels/',
        'Matchs':'0.0.0.0:8080/playground/soccer/admin/matchs/',
        'MemberAbility':'0.0.0.0:8080/playground/soccer/admin/member_ability/',
        'MemberHistory':'0.0.0.0:8080/playground/soccer/admin/member_history/',
        'Members':'0.0.0.0:8080/playground/soccer/admin/members/',
        'Nations':'0.0.0.0:8080/playground/soccer/admin/nations/',
        'Positions':'0.0.0.0:8080/playground/soccer/admin/nations/',
        'Roles':'0.0.0.0:8080/playground/soccer/admin/positions/',
        'Stadiums':'0.0.0.0:8080/playground/soccer/admin/stadiums/',
        'Teams':'0.0.0.0:8080/playground/soccer/admin/teams/',
        'Users':'0.0.0.0:8080/playground/soccer/admin/users/',
    }
METHODS = ['GET', 'POST', 'PUT', 'DELETE']

LEVELS = collections.OrderedDict()
LEVELS['name']=''

NATIONS = collections.OrderedDict()
NATIONS['name']=''

STADIUMS = collections.OrderedDict()
STADIUMS['name']=''
STADIUMS['nation']=''
STADIUMS['city']=''

TEAMS = collections.OrderedDict()
TEAMS['name']=''
TEAMS['coach']=''
TEAMS['date']=''
TEAMS['league']=''
TEAMS['stadium']=''
TEAMS['mmr']=''

MODLES = {
        'Levels' : LEVELS,
        'Nations' : NATIONS,
        'Stadiums' : STADIUMS,
        'Teams' : TEAMS
        }


def curl_post(url, data, cookie):
    c = pycurl.Curl()
    #b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
    #c.setopt(pycurl.WRITEFUNCTION, b.write)
    #Cookie disabled : logging file
    #c.setopt(pycurl.COOKIEFILE, cookie)
    #c.setopt(pycurl.COOKIEJAR, cookie)
    #c.setopt(pycurl.USERPWD, username+":"+password)
    c.setopt(pycurl.POSTFIELDS, data)
    c.perform()
    #html = b.getvalue()
    #b.close()
    c.close()
    #return html

def curl_get(url, cookie):
    c = pycurl.Curl()
    #b = StringIO.StringIO()
    c.setopt(pycurl.URL, url)
    #c.setopt(pycurl.WRITEFUNCTION, b.write)
    #Cookie disabled : logging file
    #c.setopt(pycurl.COOKIEFILE, cookie)
    #c.setopt(pycurl.COOKIEJAR, cookie)
    c.perform()
    #html = b.getvalue()
    #b.close()
    c.close()
    #return html

def print_menu():
    idx = 1
    print('-' * 100)
    for key, value in URLS.items():
        print('%2d|%20s|%s' % (idx, key, value))
        idx += 1
    print('-' * 100)

def print_method():
    idx = 1
    print('-' * 100)
    for method in METHODS:
        print('%2d|%20s' % (idx, method))
        idx += 1
    print('-' * 100)

def get_config(val):
    idx = 1
    for key, value in URLS.items():
        if idx == int(val):
            return key, value
        idx += 1
    return False

def get_method(val):
    return METHODS[int(val)-1]

def get_data_struct(model):
    return MODLES[model].copy()

def get_data(model, path):
    data = []
    ''' Return type is json'''
    if os.path.exists(path):
        real_path = os.path.realpath(path)
        file = open(real_path, 'r', encoding='utf8')
        for line in file.readlines():
            row = line.replace('\n','').split(',')
            d = get_data_struct(model)
            for i, (key, value) in enumerate(d.items()):
                d[key] = row[i]
            data.append(d)
            #d = get_data_struct(model)
            #d['name'] = line.replace('\n','')
            #data.append(d)
    return data

#Check things like below
# 1. Python Version
# 2. Argument : file at post


path = sys.argv[1]


try:

    print_menu()
    model, url = get_config(input("Select the menu: "))
    
    print_method()
    method = get_method(input("Select the method: "))

    datas = get_data(model, path)

    print(url)
    print(method)
    print(datas)

    if method == 'GET':
        curl_get(url, 'COOKIE')
    elif method == 'POST':
        for data in datas:
            curl_post(url, json.dumps(data), 'COOKIE')
        curl_get(url, 'COOKIE')
    else :
        print("Not supported yet")
except Exception as e:
    print(e)
    exit(-1)

exit(1)

if len(sys.argv) > 1:
    path = sys.argv[1]
else:
    exit(1)

print ("-" * 50)
print ("Input file : " + path)
print ("-" * 50)


if os.path.exists(path):
    real_path = os.path.realpath(path)
    file = open(real_path, 'r', encoding='utf8')
    for line in file.readlines():
        try:
            url = '0.0.0.0:8080/playground/soccer/admin/nations/' #URL should be modifed by dictionary
            data = {'name' : line.replace('\n', '')}
            curl_post(url, json.dumps(data), "COOKIE")
        except Exception as e:
            print (str(e))

