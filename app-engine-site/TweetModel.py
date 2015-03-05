from google.appengine.ext import ndb
class Tweet(ndb.Model):
    content = ndb.StringProperty(indexed=False)
    username = ndb.StringProperty(indexed=False)
    coordinates = ndb.StringProperty(indexed=False)
    source = ndb.StringProperty(indexed=False)
    tid = ndb.IntegerProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
