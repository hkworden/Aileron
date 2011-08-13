import string

from google.appengine.ext import webapp

class Page(webapp.RequestHandler):
  
  HTML_HEADER = (
      '</html>'
      '<head>'
      '<title>%s</title>%s%s'
      '</head>'
      '<body%s>'
      )
  
  HTML_FOOTER = (
      '</body>'
      '</html>'
      )
  
  def print_page_header(self, title, css_files = [], js_files = [], \
        onload=None):
    css_links = []
    for css_file in css_files:
      css_links.append('<link rel="stylesheet" text="text/css" href="%s"/>' % \
          (css_file))
    css_str = string.join(css_links)
    js_links = []
    for js_file in js_files:
      js_links.append('<script src="%s" type="text/javascript"></script>' % \
          (js_file))
    js_str = string.join(js_links)
    if onload == None:
      onload_str = ''
    else:
      onload_str = ' onload="%s"' % (onload)
    self.response.out.write(Page.HTML_HEADER % (title, css_str, js_str, \
        onload_str))
  
  def print_page_footer(self):
    self.response.out.write(Page.HTML_FOOTER)
