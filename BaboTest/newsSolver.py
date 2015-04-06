from getTasks import getTasks
from tasksParser import *
import tweepy
import time
from multiprocessing import Process

def tracking(track):
    sapi = tweepy.streaming.Stream(auths[4], CustomStreamListener())
    sapi.filter(track = track)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        try:
            tid = status.id_str
            usr = status.author.screen_name.strip()
            txt = status.text.strip()
            txt_lower = txt
            src = status.source.strip()
            cat = status.created_at
        except Exception as e:
            # Most errors we're going to see relate to the handling of UTF-8 messages (sorry)
            print(e)

        print usr + " : "
        print txt.encode('utf-8')
        for task in tasks:
            print 'RELEVANCE to the task %i: %i' % (task['ID'], getTweetRelevance(task,txt))

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

    def on_disconnect(self, notice):
        print notice
        return True # Don't kill the stream

def main(p):

    while True:
        time.sleep(50)
        tasks = getTasks()
        for i in range(len(tasks)):
            print tasks[i]['text']
        track = []
        for i,task in enumerate(tasks):
            taskInfo = parseTask(task)
            track += taskInfo['searchKeywords']
        p.terminate()
        p.join()
        p = Process(target=tracking, args=(track,))
        p.start()


if __name__ == "__main__":

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

    tasks = getTasks()
    for i in range(len(tasks)):
        print tasks[i]['text']
    task_ids = [task["ID"] for task in tasks]
    track = []

    for i,task in enumerate(tasks):
        taskInfo = parseTask(task)
        track += taskInfo['searchKeywords']

    p = Process(target=tracking, args=(track,))
    p.start()

    main(p)
