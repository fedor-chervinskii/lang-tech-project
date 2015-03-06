# -*- coding: utf-8 -*-
import tweepy as tweepy
import json
import time
#import sqlite3
from datetime import datetime
import sys
#import matplotlib.pyplot as plt
#from drawnow import drawnow
from alchemyapi import AlchemyAPI
from TweetModel import Tweet

alchemyapi = AlchemyAPI()

def getTargetedSentiment(myText, myKeyword, APIobject):
    response = APIobject.sentiment_targeted('text', myText.lower(), myKeyword)
    if response['status'] == 'OK':
        if 'score' in response['docSentiment']:
            return response['docSentiment']['type'],response['docSentiment']['score']
    else:
        print('Error in targeted sentiment analysis call: ', response['statusInfo'])

def getSentiment(myText, APIobject):
    response = APIobject.sentiment('text', myText)
    if response['status'] == 'OK':
        if 'score' in response['docSentiment']:
            return response['docSentiment']['type'],response['docSentiment']['score']
    else:
        print('Error in sentiment analysis call: ', response['statusInfo'])

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

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            if status.coordinates:
                coord = status.coordinates['coordinates']
            else:
                coord = [37.619899, 55.753301] #center of Moscow
            src = status.source.strip()
            cat = status.created_at
            score = 0

            #writing to json
            #format: [{"location":[long, lat],"text":"tweet text","score":0.7},{"location":[long, lat],"text":"tweet text 2","score":0.3}]

            # with open(json_filename,'r') as json_file:
            #     json_data = json.load(json_file)
            # json_data.append({'location': coord, 'text': txt, 'created_at': cat, 'score': score})
            # with open(json_filename,'w') as json_file:
            #     json_file.write(json.dumps(json_data, cls=DateTimeEncoder))

            tweet = Tweet()
            tweet.content = content
            tweet.username = username
            tweet.coordinates = coordinates
            tweet.source = source
            tweet.tid = tid
            tweet.put()

            # sqlite database
            # curs.execute("insert into tweets (tid, username, created_at, content, coordinates, source) values(?, ?, ?, ?, ?, ?)", (tid, usr, cat, txt, str(coord), src))
            # conn.commit()
        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

        print ('something')
        print usr + ":"
        print txt + '   '  #+ str(getSentiment(status.text,alchemyapi))
        try:
            print coord
        except:
            print 'coordinates are not defined'
        print ''

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream



    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream


def main():

    auths = []

    tweet = Tweet()
    tweet.content = "NIKITA is here"
    tweet.username = "Moscow"
    tweet.coordinates = "[37.722115, 55.542415]"
    tweet.source = "888"
    tweet.tid = 777
    tweet.put()
    #json_filename = 'tweets.json'
    for i in range(5):
        auth = tweepy.OAuthHandler(CONSUMER_KEY[i], CONSUMER_SECRET[i])
        auth.set_access_token(OAUTH_TOKEN[i], OAUTH_TOKEN_SECRET[i])
        auths.append(auth)

    # with open(json_filename, 'w') as json_file:
    #     json_file.write(json.dumps([], cls=DateTimeEncoder))

    #curs.execute("CREATE TABLE tweets (tid integer, username text, created_at text, content text, coordinates text, source text)")

    up = 55.96
    down = 55.49
    right = 37.97
    left = 37.32

    sapi = tweepy.streaming.Stream(auths[3], CustomStreamListener())
    sapi.filter(locations=[left, down, right, up])


if __name__ == "__main__":
    # conn = sqlite3.connect('tweets.db')
    # curs = conn.cursor()
    main()
