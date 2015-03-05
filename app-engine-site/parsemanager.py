from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import geotwitter
import logging

class ParseHandler(webapp.RequestHandler):
  def get(self):
      geotwitter.main()
  def post(self):
      geotwitter.main()

logging.error('Before')
application = webapp.WSGIApplication([('/parsing', ParseHandler)],
                                     debug=True)
logging.error('After')

if __name__ == '__main__':
  run_wsgi_app(application)
