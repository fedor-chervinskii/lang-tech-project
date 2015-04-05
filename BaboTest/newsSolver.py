from getTasks import getTasks
from tasksParser import *
tasks = getTasks()
for i,task in enumerate(tasks):
    taskInfo = parseTask(task)
    print taskInfo['searchKeywords']
    #geoTwitter(taskInfo["searchKeywords"])
