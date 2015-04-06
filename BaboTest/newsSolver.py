from getTasks import getTasks
from tasksParser import *
import time
from multiprocessing import Process
from CustomStreamListener import *
from operator import itemgetter

class NewsSolver():

    def run(self):
        self.auths = initAPIKeys()
        self.main()

    def main(self):

        while True:
            self.tasks = getTasks()
            self.printTasks()

            task_ids = [task["ID"] for task in self.tasks]
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


    def getKeywordsForStreaming(self):
        keyWords = []

        for i,task in enumerate(self.tasks):
            taskInfo = parseTask(task)
            keyWords += taskInfo['searchKeywords']
        return keyWords

    def updateTopTweetsWithTweet(self, tweet, tweetRank, task):
        #Update twitter list if it's full
        if len(task["topTweets"]) == 5:
            curretRankLowerBound = task["topTweets"][-1]["rank"]

            if tweetRank >=curretRankLowerBound:
                task["topTweets"][-1] = {"tweet":tweet,
                                             "rank":tweetRank}
        #Or just add it to the end of the list
        else:
            task["topTweets"].append({"tweet":tweet,
                                      "rank":tweetRank})

        #Sort the list by rank
        task["topTweets"] = sorted(task["topTweets"], key=itemgetter('rank'))
        self.printTaskTopTweet(task)

    def handleNewTweet(self, tweet):

        print tweet.userID
        print tweet.text
        if len(tweet.location) != 0:
            tweet.apilocation = getLocationCoordinates(tweet.location)

        for task in self.tasks:
            tweetRank = getTweetRelevance(task, tweet)
            self.updateTopTweetsWithTweet(tweet, tweetRank, task)
            #print 'RELEVANCE to the task %i: %i' % (task['ID'], getTweetRelevance(task, tweet))

solver = NewsSolver()
solver.run()
