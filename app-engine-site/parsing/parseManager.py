from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import geotwitter

class ParseXMLHandler(webapp.RequestHandler):
  def get(self):
      geotwitter()

application = webapp.WSGIApplication([('/path/to/cron', ParseXMLHandler)],
                                     debug=True)
if __name__ == '__main__':
  run_wsgi_app(application)