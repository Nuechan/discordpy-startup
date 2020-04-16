import discord
import time
import math
import requests
import json
import re
import urllib.request
import datetime
import sys
import os
from pytz import timezone
import emoji

client = discord.Client()
user = []
start = [0]*10
end = [0]*10

# OWM
apiKey = "12de9d40576cc2bb1c244142af408804"
baseUrl = "http://api.openweathermap.org/data/2.5/forecast?"


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # 会話
    if message.content.startswith("おは"):
        m = "はよー、" + message.author.name
        await message.channel.send(m)

    if message.content.startswith("将棋ウォーズ"):
        m = "麻雀しろよな！"
        await message.channel.send(m)

    # 計測
    if message.content.startswith("勉強開始"):
        if message.author.id in user:
            start[user.index(message.author.id)] = time.time()
            m = "アタシが計測してやる"
            await message.channel.send(m)
            end[user.index(message.author.id)] = 0
        else:
            user.append(message.author.id)
            start[user.index(message.author.id)] = time.time()
            m = "アタシが計測してやる"
            await message.channel.send(m)
            end[user.index(message.author.id)] = 0

    if message.content.startswith("勉強終了"):
        if message.author.id in user:
            if end[user.index(message.author.id)] == "end":
                m = "まずは勉強始めろよな！"
                await message.channel.send(m)
            else:
                end[user.index(message.author.id)] = time.time()
                elapsed_time = (end[user.index(message.author.id)] - start[user.index(message.author.id)]) / 60
                m =message.author.mention + str(math.floor(elapsed_time)) + "分だ！"
                await message.channel.send(m)
                end[user.index(message.author.id)] = "end"
        else:
            m = "まずは勉強始めろよな！"
            await message.channel.send(m)

    #天気
    reg_res = re.compile(u"(.+)の天気").search(message.content)
    if reg_res:
        completeUrl = baseUrl + "appid=" + apiKey + "&units=metric&lang=ja&q=" + reg_res.group(1)
        response = requests.get(completeUrl)
        cityData = response.json()
        if cityData["cod"] != "404":
            i = 1
            for item in cityData['list']:
                forecastDatetime = timezone(
                    'Asia/Tokyo').localize(datetime.datetime.fromtimestamp(item['dt']))
                weatherDescription = item['weather'][0]['description']
                temperature = item['main']['temp']
                rainfall = 0
                if 'rain' in item and '3h' in item['rain']:
                    rainfall = item['rain']['3h']
                m = (str(forecastDatetime).replace(':00+09:00', '').replace('2020-', '')).ljust(14) + ("天気：" + weatherDescription).ljust(15) + (":thermometer: " + str(math.floor(temperature))+"℃").ljust(20) + (":droplet: " + str(rainfall)+"mm")
                await message.channel.send(m)
                if i == 5:
                    break
                i = i+1
        else:
            m = "知るかバカ！"
            await message.channel.send(m)



client.run("Njk4MzIwMjA5NjM4OTgxNzYy.XpERlg.QdyimKmrn_op_obJREIyZ4TK3yQ")
