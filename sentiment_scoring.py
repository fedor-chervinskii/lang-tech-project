# -*- coding: utf-8 -*-
import time
import sqlite3
from datetime import datetime
import pandas as pd
import sys
import re
import json
from alchemyapi import AlchemyAPI

def getSentiment(myText, APIobject):
    URLless_txt = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', myText)
    Nickless_txt = ' '.join([word for word in URLless_txt.split() if not word.startswith('@')])
    response = APIobject.sentiment('text', Nickless_txt)
    if response['status'] == 'OK':
        if 'score' in response['docSentiment']:
            return response['docSentiment']['type'],response['docSentiment']['score']
    if response is None:
        print ('error')
        response = (u'None', u'0')

def smile_check(myText):
    emostr = []
    b = myText.encode('unicode_escape').split('\\')
    c = [point.replace('000','+').upper() for point in b if len(point) > 8 and point[0] == 'U']
    [emostr.append(emo_db[emo[:7]]) for emo in c if emo[:7] in emo_db]
    return emostr

def get_score(txt):
    time.sleep(0.2)
    try:
        response = getSentiment(txt + ' '.join(smile_check(txt)), alchemyapi)
        try:
            return float(response[1])
        except:
            print response
            return None
    except Exception as e:
        print(e)
        return 0

def main():
    data = pd.read_sql("SELECT * from tweets",conn)
    scores = []
    for i in data.index:
        txt = data.content[i]
        score = get_score(txt)
        scores.append(score)
        try:
            print 'tweet #%i scoring %.2f %s' % (i,score,txt)
        except:
            print 'tweet #%i scoring None %s' % (i,txt)
    data['score'] = scores
    con = sqlite3.connect('tweets_nemtsov2_scored.db')
    data.to_sql('tweets',con,index = False)
    conn.close()

if __name__ == "__main__":

    emo_json = open('emoji_database','r')
    emo_db = json.load(emo_json)
    conn = sqlite3.connect('tweets_nemtsov2.db')
    alchemyapi = AlchemyAPI()
    main()
