import urllib2
import json
def getTasks():
    req = urllib2.Request("http://api.lifenews.babo.com/tasks")
    req.add_header('LN-Device-Identifier','test')
    tasks = json.loads(urllib2.urlopen(req).read())["tasks"]
    return tasks
