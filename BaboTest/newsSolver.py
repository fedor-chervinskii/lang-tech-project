from getTasks import getTasks
from tasksParser import *
import time
from multiprocessing import Process
from CustomStreamListener import *

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

    def getKeywordsForStreaming(self):
        keyWords = []

        for i,task in enumerate(self.tasks):
            taskInfo = parseTask(task)
            keyWords += taskInfo['searchKeywords']
        return keyWords


    def handleNewTweet(self, tweet):
        for task in self.tasks:
            print 'RELEVANCE to the task %i: %i' % (task['ID'], getTweetRelevance(task, tweet))

solver = NewsSolver()
solver.run()
