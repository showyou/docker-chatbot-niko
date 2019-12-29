#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import datetime
from   sqlalchemy import and_
import random

# /home/*/hama_dbとかが返ってくる
#exec_path = os.path.abspath(os.path.dirname(__file__)).rsplit("/",1)[0]
exec_path = "."
conf_path = exec_path+"/common/config.json"
sys.path.insert(0,exec_path)
from common import auth_api, model
import tweepy


#格納しないテキストのリスト
g_ngTrend = [ 
        "オフパコ",
        "フルチン"
]


dbSession = None


def get_auth_data(fileName):
    file = open(fileName,'r')
    a = json.loads(file.read())
    file.close()
    return a


# NGUserならTrue そうでないならFalse 
def is_ng_trend(trend):
    if trend in g_ngTrend: return True
    return False


"""
    テキストが適合している = True
    重複してたり、RTだったり = False
"""
def check_text(text, dbSession):
     
    if( is_ng_trend(text) ): return False
    #jTime = created_at + datetime.timedelta(hours = 9)

    query = dbSession.query(model.Trend).filter(
        model.Trend.text == text
    )
    if( query.count() > 0 ): return False

    #ここに品詞判定辺り入れる

    t = model.Trend()
    t.text = text
    #t.datetime = jTime
    dbSession.add(t)
    return True


def main():

    # twitterから発言を取ってきてDBに格納する
    userdata = get_auth_data(conf_path)
    tw = auth_api.connect(userdata["consumer_token"],
        userdata["consumer_secret"], exec_path+"/common/")
    #print tw.rate_limit_status()
    dbSession = model.startSession(userdata)

    page_number = 0
    update_flag = True
    while update_flag:
        update_flag = False
        page_number += 1
        if page_number > 1: break

        #l = tw.home_timeline(page = page_number, count=10)
        #Toyko座標ベタ打ち
        woeid = tw.trends_closest(35.652832, 139.839478)[0]['woeid']
        trends_place = tw.trends_place(woeid)
        l = trends_place[0]['trends']
        for s in l:
            trend = s['name']
            if trend.startswith("#"): trend = trend[1:]
            #print(trend)
            update_flag = check_text(trend, 
                    dbSession)
            if(not(update_flag)): continue
            try:
                tw.update_status("な、なによ……! ニコだって" + trend +\
                        "くらいできるんだから！！")
                print("trend "+trend)
            except tweepy.TweepError:
                pass
            #print("flag: ", update_flag)
            if update_flag: break
        dbSession.commit()
        

if __name__ == "__main__":
    main()
