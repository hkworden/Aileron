import string

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from data.model.station import Station
from views.page import Page

class IndexPage(Page):
  
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    write = self.response.out.write
    self.write_header()
    self.write_station_options(write)
    self.write_footer()
  
  def write_header(self):
    css_files = ['css/chosen.css']
    js_files = ['js/jquery.min.js', 'js/chosen.jquery.min.js', 'js/index.js']
    self.print_page_header('Aileron', css_files, js_files, 'main();')
  
  def write_footer(self):
    self.print_page_footer()
  
  def write_station_options(self, write):
    write('<select class="chzn-select" style="width:350px;">')
    q = Station.all()
    q.order('display_name')
    for station in q:
      write('<option data-link="/s/%s">%s (%s)</option>' % \
          (station.key().id(), station.display_name, \
          string.join(station.trains, '/')))
    write('</select>')

application = webapp.WSGIApplication([('/?', IndexPage)], debug=True)

def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
