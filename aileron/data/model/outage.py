from google.appengine.ext import db
from station import Station

class Outage(db.Model):
  station = db.ReferenceProperty(Station)
  equipment_id = db.StringProperty()
  equipment_type = db.IntegerProperty()
  equipment_serving = db.StringProperty()
  equipment_is_ada = db.BooleanProperty()
  reason = db.StringProperty()
  start_date = db.DateTimeProperty()
  est_end_date = db.DateTimeProperty()
  end_date = db.DateTimeProperty()

class EquipmentType:
  ELEVATOR = 1
  ESCALATOR = 2
  UNKNOWN = -1
  @staticmethod
  def abbrev_to_code(abbrev):
    if abbrev == 'EL':
      return EquipmentType.ELEVATOR
    if abbrev == 'ES':
      return EquipmentType.ESCALATOR
    return EquipmentType.UNKNOWN
