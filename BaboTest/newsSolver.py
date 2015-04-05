import getTasks
import tasksParser as tasksParser
tasks = getTasks()
for i,task in enumerate(tasks):
    taskInfo = tasksParser.parseTask(task)
    //geoTwitter(taskInfo["searchKeywords"])
