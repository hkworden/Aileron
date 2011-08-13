from google.appengine.ext import db
from station import Station

class Equipment(db.Model):
  station = db.ReferenceProperty(Station)
  mta_id = db.StringProperty()
  equipment_type = db.IntegerProperty()
  serving = db.StringProperty()
  is_ada = db.BooleanProperty()

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
