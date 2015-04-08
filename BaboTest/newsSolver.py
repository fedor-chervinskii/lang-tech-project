from getTasks import getTasks
from tasksParser import *
import time
from multiprocessing import Process
from CustomStreamListener import *
from operator import itemgetter
import csv

class NewsSolver():

    def run(self):
        self.tasks = []
        self.auths = initAPIKeys()
        self.main()

    def main(self):

        while True:
            self.updateTasks()
            self.printTasks()

            streamingKeywords = self.getKeywordsForStreaming()

            process = Process(target=tracking, args=(streamingKeywords, self.auths, self))
            process.start()

            time.sleep(50)

            process.terminate()
            process.join()

    def printTasks(self):
        for i in range(len(self.tasks)):
            print self.tasks[i]['text']

    def printTaskTopTweet(self, task):
        print ''
        print 'Task: ' + task['text']
        print 'Top Tweet: ' + task["topTweets"][0]["tweet"].text
        print ''
    def saveTopTweetsOfTask(self, task):
        #writer = csv.writer(open(filepath,'wb'))
        with open("task{}.tsv".format(task["ID"]), 'wb') as f:
            for tweet in task["topTweets"]:
                f.write("{0}\t{1}\n".format(tweet["tweet"].text.encode("utf-8"), tweet["rank"]))

    def updateTasks(self):
        currentTaks = getTasks()
        tasksIds = [task["ID"] for task in self.tasks]
        [self.tasks.append(task) for task in currentTaks if task["ID"] not in tasksIds]

    def getKeywordsForStreaming(self):
        keyWords = []

        for i,task in enumerate(self.tasks):
            taskInfo = parseTask(task)
            keyWords += taskInfo['searchKeywords']
        return keyWords

    def updateTopTweetsWithTweet(self, tweet, tweetRank, task):
        updatedRating = False
        #Update twitter list if it's full
        if len(task["topTweets"]) == 5:
            curretRankLowerBound = task["topTweets"][-1]["rank"]

            if tweetRank >=curretRankLowerBound:
                task["topTweets"][-1] = {"tweet":tweet,
                                             "rank":tweetRank}
                updatedRating = True
        #Or just add it to the end of the list
        else:
            task["topTweets"].append({"tweet":tweet,
                                      "rank":tweetRank})
            updatedRating = True

        #Sort the list by rank
        if updatedRating == True:
            task["topTweets"] = sorted(task["topTweets"], key=itemgetter('rank'))
            self.printTaskTopTweet(task)
            self.saveTopTweetsOfTask(task)

    def processGeodata(self, tweet):
        if tweet.geodata is not None:
            geodata = tweet.geodata['coordinates']
            tweet.trueLocation = {'lat':geodata[0], 'lon':geodata[1]}
        elif len(tweet.location):
            apiResponse = getLocationCoordinates(tweet.location)
            tweet.trueLocation['lat'] = apiResponse['lat']
            tweet.trueLocation['lon'] = apiResponse['lng']
            tweet.trueLocation['text'] = apiResponse['formatted_address']
        else:
            tweet.trueLocation = None

    def handleNewTweet(self, tweet):

        print tweet.userID
        print tweet.text
        self.processGeodata(tweet)

        for task in self.tasks:
            tweetRank = getTweetRelevance(task, tweet)
            self.updateTopTweetsWithTweet(tweet, tweetRank, task)
            #print 'RELEVANCE to the task %i: %i' % (task['ID'], getTweetRelevance(task, tweet))

solver = NewsSolver()
solver.run()
