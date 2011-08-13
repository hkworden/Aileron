from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from data.model.outage import Outage
from data.model.station import Station

class InfoStationPage(webapp.RequestHandler):
  
  def get(self, sid):
    station = self.get_station(sid)
    self.response.headers['Content-Type'] = 'text/plain'
    write = self.response.out.write
    self.print_station_info(write, station)
    self.print_outage_info(write, station)
  
  def get_station(self, sid):
    sid = int(sid)
    return Station.get_by_id(sid)
  
  def print_station_info(self, write, station):
    write(station.display_name + '\n')
  
  def print_outage_info(self, write, station):
    q = Outage.all()
    q.filter('end_date = ', None)
    q.filter('station = ', station)
    if q.count() == 0:
      write('No known problems.\n')
    else:
      for outage in q:
        write('outage\n')

application = webapp.WSGIApplication([(r'/s/(.*)', InfoStationPage)], \
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
