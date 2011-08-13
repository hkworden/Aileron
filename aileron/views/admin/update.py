import httplib
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from data.updater import Updater

class UpdatePage(webapp.RequestHandler):
  
  STATUS_PAGE_HOST = 'mta.info'
  STATUS_PAGE_PATH = '/developers/data/nyct/nyct_ene.xml'
  
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    con = httplib.HTTPConnection(UpdatePage.STATUS_PAGE_HOST)
    con.request('get', UpdatePage.STATUS_PAGE_PATH)
    data = con.getresponse().read()
    con.close()
    updater = Updater(self.response.out.write)
    updater.update_data(data)

application = webapp.WSGIApplication([('/_admin/update/?', UpdatePage)], \
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
