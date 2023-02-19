#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tagsBot.py
import requests
import datetime
from tagsConfig import *
from collections import Counter
from blacklist import *
global id
global pagination
global tags
import sys
id = ""
pagination = ""
tags = []


testing = False

if testing:
    game = 'Minecraft'
else:
    game = input("Please enter category:")

def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds


def getMoreStreams():
    try:
        global pagination
        global id
        global gameViewers
        global gameStreams
        global medianList
        global dropsGames
        urlMore = "https://api.twitch.tv/helix/streams?first=100&language=en&language=other&game_id=" + id + "&after=" + pagination
        paramsMore = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
        r = requests.get(urlMore, headers=paramsMore).json()
        if not r['pagination'] == {}:
            pagination = r['pagination']['cursor']
            for a in r['data']:
                startedAt = a['started_at']
                year, month, day, hour, minute, second = int(startedAt[0:4]), int(startedAt[5:7]), int(startedAt[8:10]), int(startedAt[11:13]), int(startedAt[14:16]), int(startedAt[17:19])
                startedAt = datetime.datetime(year, month, day, hour, minute, second)
                now = datetime.datetime.now()
                hours, minutes, seconds = convert_timedelta(now - startedAt)
                if not hours > 18:
                    if not a['tags'] is None:
                        for t in range(len(a['tags'])):
                            tags.append(a['tags'][t])
            getMoreStreams()
    except Exception as x:
        print(x)
    except requests.exceptions.ConnectTimeout:
        print("timeout", urlMore)


url = "https://api.twitch.tv/helix/games?name=" + game
params = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
r = requests.get(url, headers=params).json()
id = r['data'][0]['id']
getMoreStreams()

c = Counter(tags)

keys = list(c.keys())
values = list(c.values())

for k in range(len(keys)):
    for d in range(len(keys)):
        if not keys[k] == keys[d]:
            if keys[k].lower() == keys[d].lower():
                values[k] = values[k] + values[d]
                keys[d] = 'x'
                values[d] = 0

newKeys = []
newValues = []

for i in range(len(keys)):
    newKeys.append(keys[i])
    newValues.append(values[i])

dummy = []
dummy[:], newKeys[:] = zip(*sorted(zip(newValues, newKeys), key=lambda p: (p[0], p[1])))
newValues = sorted(newValues[:])

for i in range(len(newKeys)):
    if testing:
        if not newKeys[i].lower() in (tag.lower() for tag in ridgureBlacklist):
            if not newValues[i] == 0:
                print(newValues[i], newKeys[i])
    else:
        if str(sys.argv[1]) == '-ridgureBlacklist':
            if not newKeys[i].lower() in (tag.lower() for tag in ridgureBlacklist):
                if not newValues[i] == 0:
                    print(newValues[i], newKeys[i])
        elif str(sys.argv[1]) == '-noBlacklist':
            if not newValues[i] == 0:
                print(newValues[i], newKeys[i])
        elif str(sys.argv[1]) == '-ririTheDinoBlacklist':
            if not newKeys[i] in ririBlacklist:
                if not newValues[i] == 0:
                    print(newValues[i], newKeys[i])

