# -*- coding: utf-8 -*-
import tweepy
import numpy as np
import json
import time
import sqlite3
import send_email
from datetime import datetime

from alchemyapi import AlchemyAPI

use = 0
alchemyapi = AlchemyAPI(use = use)

import time, threading

def updateCounter():
  global use
  global alchemyapi
  print use
  use += 1
  if use >= 15:
    use = 0
  alchemyapi = AlchemyAPI(use = use)
threading.Timer(100, updateCounter).start()

updateCounter()

#def getTargetedSentiment(myText, myKeyword, APIobject):
#    response = APIobject.sentiment_targeted('text', myText, myKeyword)
#    if response['status'] == 'OK':
#        if 'score' in response['docSentiment']:
#            return response['docSentiment']['type'],response['docSentiment']['score']
#    else:
#        print('Error in targeted sentiment analysis call: ', response['statusInfo'])
#
def getSentiment(myText, APIobject):
    response = APIobject.sentiment('text', myText)
    if response['status'] == 'OK':
        if 'score' in response['docSentiment']:
            return response['docSentiment']['type'],response['docSentiment']['score']
    else:
        print('Error in sentiment analysis call: ', response['statusInfo'])

def smile_check(myText):
    emostr = []
    b = myText.encode('unicode_escape').split('\\')
    c = [point.replace('000','+').upper() for point in b if len(point) > 8 and point[0] == 'U']
    [emostr.append(emo_db[emo[:7]]) for emo in c if emo[:7] in emo_db]
    return emostr

def get_score(txt):
    try:
        response = getSentiment(txt + ' '.join(smile_check(txt)), alchemyapi)
        try:
            return float(response[1])
        except:
            return 0
    except Exception as e:
        print(e)
        return 0

#Some access keys
CONSUMER_KEY = ['KpfGPpsl5Dn03Lb5wzvQfEaMc',
                '13AqFSrFdFv7rdLVOGvzJCkmp',
                '45RuEYLg5eVTYyEGuyEerplyY',
                '3qTMdAYKxctRe69HMDqyeNST2',
                'JJkrFkKGlhDIEgj2eTrQ']

CONSUMER_SECRET = ['UWRvjR3CHsducO1i7268F24C3M9UJu5U7p2u4kh6Ds6QMDdKCg',
                   'LVaOSMsMBWl4FmgthjNPWMnkKe7MXKXrmu5uL6JnJWIhHieDxR',
                   'LBnbBTIAhtYYBU6RWeyCzgIcJannob7bPrzg3dMqFuRDLJnbHp',
                   'Jwwv3wHzL2jtYMHylakpjmDxf5SgvAwexFGfEoCFHw92f65lnK',
                   'H7hmUQXqXseKbj1WnKFMnaURyQbBaDeyK3DAAwLI']

OAUTH_TOKEN = ['2181757628-o8IOmHBelyhVM6KEkkT50ZLIbv4fj6llW6KSjpd',
               '175663996-ZNL1MivJASYSxWsNXlxNHnQhmLHDegH9VdVfATsL',
               '175663996-lQRf1JNjvR1fVILTtoEH4FHVQ1sLtPa0IIa8lMog',
               '2841198550-rlPUcMyCj8rk3Yv6XxGJWk0ELCCUGUrxhvYyAa6',
               '2181757628-0n3FpGEtoob0qum7IMeN3R0oV1kg5STZwmXNa9Q']

OAUTH_TOKEN_SECRET = ['cyLlZtQyv4rgcWA5pGaXLtGJaFqD4PGOlxSdb4ECVzoSP',
                      'gJOHvvlcObkiu7Qd91WapTFwnOVsisdoeMBUHxcFfzBac',
                      'eQ0SUwziSUgRs72HJzWpU9IAlVP92X9YJsGHOPrWUctw3',
                      '9b36g1wXLzn1yB0FGIoT9eACxPPpaZVfESnmRYcDYk3wv',
                      'MqgrZHb8CMyNqFJn36YmCtLUQ5rqNUzX2IxWNfQdHQ6t7']

auths = []

for i in range(5):
    auth = tweepy.OAuthHandler(CONSUMER_KEY[i], CONSUMER_SECRET[i])
    auth.set_access_token(OAUTH_TOKEN[i], OAUTH_TOKEN_SECRET[i])
    auths.append(auth)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

#conn = sqlite3.connect('tweets.db')
#curs = conn.cursor()

#uncomment the following in case of the first launch

#curs.execute("CREATE TABLE tweets (tid integer, username text, created_at text, content text, lat real, long real, source text, month int, day int, hour int, hourly text, score real, content_lower text)")

#conn.close()

up = 55.96
down = 55.49
right = 37.97
left = 37.32

emo_json = open('emoji_database','r')
emo_db = json.load(emo_json)

counter = 0

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            score = getSentiment(txt,alchemyapi)
            txt_lower = txt#.lower()
	    if status.coordinates:
                print status.coordinates['coordinates']
                [lat, long] = status.coordinates['coordinates']
            else:
                [lat, long] = [37.619899, 55.753301] #center of Moscow
            src = status.source.strip()
            cat = status.created_at
            score = get_score(txt)
            month = cat.month
            day = cat.day
            hour = cat.hour
            hourly = '%i.%i %ih' % (month,day,hour)
            print hourly
            # sqlite database
            conn = sqlite3.connect('tweets.db')
            curs = conn.cursor()
            curs.execute("insert into tweets (tid, username, created_at, content, lat, long, source, month, day, hour, hourly, score, content_lower) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tid, usr, cat, txt, lat, long, src, month, day, hour, hourly, score, txt_lower))
            conn.commit()
            conn.close()
        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

        print usr + ":"
        print txt.encode('utf-8') #+ '   ' + str(getSentiment(status.text,alchemyapi))
        print score
        print ''

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        send_email.send_email('Twitter stream error on the server, check!')
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        send_email.send_email('Twitter stream timeout on the server, check!')
        return True # Don't kill the stream

    def on_disconnect(self, notice):
        print notice
        send_email.send_email('Twitter stream disconnect on the server, check!')
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auths[4], CustomStreamListener())
try:
    sapi.filter(locations=[left, down, right, up])
except:
    send_email.send_email('Smth goes wrong on the server, check!')
