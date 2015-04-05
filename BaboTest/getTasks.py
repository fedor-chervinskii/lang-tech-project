import urllib2
import json
def getTasks()
  tasks = json.loads(urllib2.urlopen("http://api.lifenews.babo.com/tasks").read())["tasks"]
  return tasks
