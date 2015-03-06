from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import geotwitter
import logging

class ParseHandler(webapp.RequestHandler):
  def get(self):
      self.response.write("HELLO GET PRE")
      geotwitter.main()
      self.response.write("HELLO GET")
  def post(self):
      self.response.write("HELLO POST PRE")
      geotwitter.main()
      self.response.write("HELLO POST")

logging.error('Before')
application = webapp.WSGIApplication([('/parser', ParseHandler)],
                                     debug=True)
logging.error('After')

if __name__ == '__main__':
  run_wsgi_app(application)
