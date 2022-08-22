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
id = ""
pagination = ""
tags = []

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
                    if not a['tag_ids'] is None:
                        for t in range(len(a['tag_ids'])):
                            tags.append(a['tag_ids'][t])
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
newKeys = []
newValues = []


for i in range(len(keys)):
    urlMore = "https://api.twitch.tv/helix/tags/streams?tag_id=" + keys[i]
    paramsMore = {"Client-ID": "" + ClientID + "", "Authorization": "Bearer " + FollowerToken}
    r = requests.get(urlMore, headers=paramsMore).json()
    if r['data'][0]['localization_names']['en-us'] == 'English':
        newKeys.append(r['data'][0]['localization_names']['en-us'])
        newValues.append(values[i])
    if not r['data'][0]['is_auto']:
        newKeys.append(r['data'][0]['localization_names']['en-us'])
        newValues.append(values[i])

dummy = []
dummy[:], newKeys[:] = zip(*sorted(zip(newValues, newKeys), key=lambda p: (p[0], p[1])))
newValues = sorted(newValues[:])

for i in range(len(newKeys)):
    if not newKeys[i] in tagsBlacklist:
        print(newValues[i], newKeys[i])
