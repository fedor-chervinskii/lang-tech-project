import os
import urllib
import cgi
import sys

import jinja2
import webapp2
import json
import time
from TweetModel import Tweet
from datetime import datetime

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            encoded_object = list(obj.timetuple())[0:6]
        else:
            encoded_object =json.JSONEncoder.default(self, obj)
        return encoded_object


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'

        tweets_query = Tweet.query().order(-Tweet.date)
        tweets = tweets_query.fetch(10)
        json_data = []
        for tweet in tweets:
            json_data.append({'location': tweet.coordinates, 'text': tweet.content, 'created_at': tweet.date, 'score': 0})
        self.response.write(json.dumps(json_data, cls=DateTimeEncoder))

application = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
