from datetime import datetime
from xml.dom.minidom import parseString

from model.equipment import Equipment, EquipmentType
from model.outage import Outage
from model.station import Station, StationName

class Updater:
  
  DT_FORMAT = '%m/%d/%Y %I:%M:%S %p'
  
  def __init__(self, write):
    self.write = write
  
  def update_data(self, data):
    self.build_existing_outage_list()
    dom = parseString(data)
    outages = dom.getElementsByTagName('outage')
    for outage in outages:
      mta_id = self.get_node_value(outage, 'equipment')
      if mta_id == None:
        # TODO
        continue
      if mta_id in self.existing_outages:
        # this outage is already in the database
        del self.existing_outages[mta_id]
        continue
      station_name = self.get_node_value(outage, 'station')
      trains_value = self.get_node_value(outage, 'trainno')
      if trains_value == None:
        # TODO: this is a problem
        continue
      trains = trains_value.split('/')
      equipment_id = self.get_node_value(outage, 'equipment')
      if equipment_id == None:
        # TODO
        continue
      equipment_type_value = self.get_node_value(outage, 'equipmenttype')
      if equipment_type_value == None:
        # TODO
        continue
      equipment_type = EquipmentType.abbrev_to_code(equipment_type_value)
      serving = self.get_node_value(outage, 'serving')
      if serving == None:
        # TODO
        continue
      is_ada_value = self.get_node_value(outage, 'ADA')
      if is_ada_value == None or (is_ada_value != 'Y' and is_ada_value != 'N'):
        # TODO
        continue
      is_ada = is_ada_value == 'Y'
      start_date_value = self.get_node_value(outage, 'outagedate')
      if start_date_value == None:
        # TODO
        continue
      start_date = datetime.strptime(start_date_value, Updater.DT_FORMAT)
      est_end_date_value = self.get_node_value(outage, \
          'estimatedreturntoservice')
      if est_end_date_value == None:
        # TODO
        continue
      est_end_date = datetime.strptime(est_end_date_value, Updater.DT_FORMAT)
      reason = self.get_node_value(outage, 'reason')
      if reason == None:
        # TODO
        continue
      equipment = self.get_equipment(equipment_id, equipment_type, \
          station_name, trains, serving, is_ada)
      outage = Outage(equipment = equipment, reason = reason, \
          start_date = start_date, est_end_date = est_end_date)
      outage.put()
    now = datetime.now()
    for outage in self.existing_outages:
      outage.end_date = now
      outage.put()
  
  def build_existing_outage_list(self):
    self.existing_outages = {}
    q = Outage.all()
    q.filter('end_date = ', None)
    count = q.count()
    outage_list = q.fetch(count)
    for outage in outage_list:
      self.existing_outages[outage.equipment.mta_id] = outage
  
  def get_equipment(self, equipment_id, equipment_type, station_name, \
      train_list, serving, is_ada):
    # trying to find equipment by the given ID
    # TODO what if IDs aren't unique, or are re-used?
    q = Equipment.all()
    q.filter('mta_id = ', equipment_id)
    count = q.count()
    if count == 1:
      return q.get()
    elif count > 1:
      # TODO: this is a problem
      return None
    station = self.get_station(station_name, train_list)
    if station == None:
      self.write('no station found for: %s\n' % (station_name))
    else:
      self.write('found %s\n' % (station.display_name))
    if station == None:
      equipment = Equipment(mta_id = equipment_id, \
          equipment_type = equipment_type, serving = serving, is_ada = is_ada)
    else:
      equipment = Equipment(station = station, mta_id = equipment_id, \
          equipment_type = equipment_type, serving = serving, is_ada = is_ada)
    equipment.put()
    return equipment
  
  def get_station(self, station_name, train_list):
    q = StationName.all()
    q.filter('name = ', station_name.lower())
    count = q.count()
    if count == 0:
      return None
    if count == 1:
      return q.get().station
    station_names = q.fetch(count)
    for sn in station_names:
      station = sn.station
      s_train_set = set(station.trains)
      a_train_set = set(train_list)
      if s_train_set != a_train_set:
        station_names.remove(sn)
    if len(station_names) == 1:
      return station_names[0].station
    else:
      return None
  
  def get_node_value(self, node, key):
    node_list = node.getElementsByTagName(key)
    if len(node_list) != 1:
      return None
    child_node_list = node_list[0].childNodes
    if len(child_node_list) != 1:
      return None
    return child_node_list[0].nodeValue
