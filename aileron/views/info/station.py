from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from data.model.outage import Outage
from data.model.station import Station
from views.page import Page

class InfoStationPage(Page):
  
  def get(self, sid):
    station = self.get_station(sid)
    self.response.headers['Content-Type'] = 'text/html'
    write = self.response.out.write
    self.write_header(station)
    self.print_station_info(write, station)
    self.print_outage_info(write, station)
    self.write_footer()
  
  def write_header(self, station):
    self.print_page_header('Aileron &raquo; %s' % (station.display_name))
  
  def write_footer(self):
    self.print_page_footer()
  
  def get_station(self, sid):
    sid = int(sid)
    return Station.get_by_id(sid)
  
  def print_station_info(self, write, station):
    write('<h2>%s</h2>' % (station.display_name))
  
  def print_outage_info(self, write, station):
    q = Outage.all()
    q.filter('end_date = ', None)
    q.filter('station = ', station)
    if q.count() == 0:
      write('No known problems.\n')
    else:
      for outage in q:
        write('outage<br/>')

application = webapp.WSGIApplication([(r'/s/(.*)', InfoStationPage)], \
    debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
