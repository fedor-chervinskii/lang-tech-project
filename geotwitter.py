# -*- coding: utf-8 -*-
import tweepy
import json
import time
import sqlite3
from alchemyapi import AlchemyAPI
import matplotlib.pyplot as plt
from drawnow import drawnow

alchemyapi = AlchemyAPI()

myText = "нас отпустили домой с физ-ры"
response = alchemyapi.sentiment("text", myText)
print "Sentiment: ", response["docSentiment"]["type"]

#[me, Segey1, Sergey2, Nastya]
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

conn = sqlite3.connect('tweets.db')
curs = conn.cursor()
#curs.execute("CREATE TABLE tweets (tid integer, username text, created_at text, content text, coordinates text, source text)")

up = 55.96
down = 55.49
right = 37.97
left = 37.32

im = plt.imread('Moscow_bigger.png')
width, height, nchannels = im.shape

def getX(lgt):
    return round(width*( lgt - left )/float( right - left ))

def getY(lat):
    return round(height*( up - lat )/float( up - down ))

plt.ion() # enable interactivity
fig = plt.figure()

def makeFig():
    plt.imshow(im)
    plt.axis([0,800,1029,0])
    plt.scatter(x,y)

x=list()
y=list()

x.append(getX((right+left)/2))
y.append(getY((down+up)/2))

drawnow(makeFig)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            if status.coordinates:
                coord = str(status.coordinates['coordinates'])
            else:
                coord = '[37.619899, 55.753301]' #center of Moscow
            src = status.source.strip()
            cat = status.created_at

            # Now that we have our tweet information, let's stow it away in our
            # sqlite database
            curs.execute("insert into tweets (tid, username, created_at, content, coordinates, source) values(?, ?, ?, ?, ?, ?)", (tid, usr, cat, txt, coord, src))
            conn.commit()
        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

        if status.coordinates :
            xpos = getX(status.coordinates['coordinates'][0])
            ypos = getY(status.coordinates['coordinates'][1])
        else :
            xpos = getX(37.62)
            ypos = getY(55.75)
        x.append(xpos)
        y.append(ypos)
        drawnow(makeFig)
        print status.user.screen_name + ":"
        print status.text
        try:
            print coord
        except:
            print 'coordinates are not defined'

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auths[1], CustomStreamListener())
sapi.filter(locations=[left, down, right, up])
