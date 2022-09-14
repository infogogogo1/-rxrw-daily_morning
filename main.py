'''
# -*- coding: utf-8 -*-
# @Time : 2022/8/25 15:03
# @Author : Haolin
# @email : cuihaolin@xinzhengjinke.com
# @File : test.py
# @Software: PyCharm
'''

from datetime import date, datetime, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now() + timedelta(hours=8)

# 新增周天判断
week_day = datetime.today().weekday()
week_list = ['周一','周二','周三','周四','周五','周六','周天']
new_week_day = week_list[week_day]
days_val = (5-week_day)
if days_val>=0:
    days_val = days_val
else:
    days_val = '0'

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
# 测试增加天气判断带祝福语,增加'°C'
  if weather['weather'] == '多云':
      weather['weather'] = '多云 (今天天上会有很好看的云朵噢！！)'
  elif weather['weather'] == '晴':
       weather['weather'] = '晴 (祝你一天好心晴！么么哒！)'
  elif weather['weather'] == '小雨':
       weather['weather'] = '小雨 (要下雨辣！！要带伞噢！别感冒了！)'
  elif weather['weather'] == '暴雨':
       weather['weather'] = '暴雨 (！有暴雨！别出门！)'
  elif weather['weather'] == '阴':
       weather['weather'] = '阴 (就算是阴天也要元气满满噢！加油)'
  else:
     pass
  return weather['weather'], str(math.floor(weather['temp']))+'°C', str(math.floor(weather['high']))+'°C', str(math.floor(weather['low']))+'°C'

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return get_words()
#   return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
data = {"city":{"value":city},
        "date":{"value":today.strftime('%Y年%m月%d日')+' '+new_week_day},  # 日期添加周几,距离周末的天数
        "write":{"value":"距离周末还有：%s天！" % days_val,"color":get_random_color()},
        "weather":{"value":wea},
        "temperature":{"value":temperature},
        "love_days":{"value":get_count()},
        "birthday_left":{"value":get_birthday()},
        "highest": {"value":highest},
        "lowest":{"value":lowest}}
count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
