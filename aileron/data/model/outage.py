from google.appengine.ext import db
from equipment import Equipment

class Outage(db.Model):
  equipment = db.ReferenceProperty(Equipment)
  reason = db.StringProperty()
  start_date = db.DateTimeProperty()
  est_end_date = db.DateTimeProperty()
  end_date = db.DateTimeProperty()
