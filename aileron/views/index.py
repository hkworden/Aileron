import string

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from data.model.station import Station

class IndexPage(webapp.RequestHandler):
  
  HTML_HEADER = (
      '</html>'
      '<head>'
      '<title>Aileron</title>'
      '<link rel="stylesheet" type="text/css" href="css/chosen.css"/>'
      '<script src="js/jquery.min.js" type="text/javascript"></script>'
      '<script src="js/chosen.jquery.min.js" type="text/javascript"></script>'
      '<script src="js/main.js" type="text/javascript"></script>'
      '</head>'
      '<body onload="main();">'
      )
  
  HTML_FOOTER = (
      '</body>'
      '</html>'
      )
  
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    write = self.response.out.write
    write(IndexPage.HTML_HEADER)
    self.write_station_options(write)
    write(IndexPage.HTML_FOOTER)
  
  def write_station_options(self, write):
    write('<select class="chzn-select" style="width:350px;">')
    q = Station.all()
    q.order('display_name')
    for station in q:
      write('<option>%s (%s)</option>' % (station.display_name, \
          string.join(station.trains, '/')))
    write('</select>')

application = webapp.WSGIApplication([('/?', IndexPage)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
