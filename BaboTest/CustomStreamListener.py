import tweepy

def tracking(track, auths,newTweetsHandler):
    sapi = tweepy.streaming.Stream(auths[4], CustomStreamListener(newTweetsHandler))
    sapi.filter(track = track)

class Tweet():
    def __init__(self,tID,uID,txt,src,cat,timezone,location,geodata):
        self.tweetID = tID
        self.userID = uID
        self.text = txt
        self.device = src
        self.createdAt = cat
        self.timezone = timezone
        self.location = location
        self.geodata = geodata

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, newTweetsHandler=None):
        super(CustomStreamListener, self ).__init__()
        self.newTweetsHandler = newTweetsHandler

    def on_status(self, status):
        try:

            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            src = status.source.strip()
            cat = status.created_at
            timezone = status.author.time_zone
            location = status.author.location.strip()
            geodata = status.coordinates
            tweet = Tweet(tid,usr,txt,src,cat,timezone,location,geodata)
            self.newTweetsHandler.handleNewTweet(tweet)

        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def on_disconnect(self, notice):
        print notice
        return True # Don't kill the stream

def initAPIKeys():
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
    return auths
