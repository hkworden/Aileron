import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from data.loader import Loader

class LoadPage(webapp.RequestHandler):
  
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(
        '<html>'
        '<head>'
        '<title>Aileron &raquo; Admin &raquo; Load Data</title>'
        '</head>'
        '<body>'
        '<form action="" method="post" enctype="multipart/form-data">'
        '<input type="file" name="in" /><br/>'
        '<input type="submit" value="Load Data" />'
        '</form>'
        '</body>'
        '</html>'
        )
  
  def post(self):
    self.response.headers['Content-Type'] = 'text/plain'
    loader = Loader(self.response.out.write)
    loader.load_data(self.request.get('in'))

application = webapp.WSGIApplication([('/_admin/load/?', LoadPage)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
