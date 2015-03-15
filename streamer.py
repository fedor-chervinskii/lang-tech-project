# -*- coding: utf-8 -*-
import tweepy
import json
import time
import sqlite3
import send_email
from datetime import datetime

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

conn = sqlite3.connect('tweets.db')
curs = conn.cursor()

#uncomment the following in case of the first launch

#curs.execute("CREATE TABLE tweets (tid integer, username text, created_at text, content text, lat real, long real, source text)")

up = 55.96
down = 55.49
right = 37.97
left = 37.32

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            if status.coordinates:
                print status.coordinates['coordinates']
		[lat, long] = status.coordinates['coordinates']
	    else:
                [lat, long] = [37.619899, 55.753301] #center of Moscow
            src = status.source.strip()
            cat = status.created_at
            score = 0

            # sqlite database
            curs.execute("insert into tweets (tid, username, created_at, content, lat, long, source) values(?, ?, ?, ?, ?, ?, ?)", (tid, usr, cat, txt, lat, long, src))
            conn.commit()
        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

        print usr + ":"
        print txt.encode('utf-8') #+ '   ' + str(getSentiment(status.text,alchemyapi))
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
sapi.filter(locations=[left, down, right, up])
