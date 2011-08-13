from google.appengine.ext import db

class Station(db.Model):
  mta_id = db.StringProperty()
  display_name = db.StringProperty()
  lat = db.FloatProperty()
  lng = db.FloatProperty()
  trains = db.ListProperty(str)

class StationName(db.Model):
  station = db.ReferenceProperty(Station)
  name = db.StringProperty()
