import logging

from model.station import Station, StationName

class Loader:
  
  def __init__(self, write):
    self.write = write
  
  def load_data(self, stations):
    self.write('loading...\n')
    rows = stations.split('\n')
    for i in range(1, len(rows) - 1):
      data = rows[i].split(',')
      if len(data) != 5:
        continue
      mta_id = data[0]
      display_name = data[1]
      lat = float(data[2])
      lng = float(data[3])
      routes = data[4].split('/')
      station = Station(mta_id = mta_id, display_name = display_name, \
          lat = lat, lng = lng, trains = routes)
      station.put()
      self.add_station_names(station)
  
  def add_station_names(self, station):
    raw_name = station.display_name.lower()
    names = []
    names.append(raw_name)
    add_funcs = [ self.make_ordinalized_name, \
                  self.make_station_appended_name ]
    for add_func in add_funcs:
      add_list = []
      for name in names:
        add_name = add_func(name)
        if name != add_name:
          add_list.append(add_name)
      names += add_list
    for name in names:
      station_name = StationName(station = station, name = name)
      station_name.put()
  
  def make_ordinalized_name(self, name):
    res = ''
    for token in name.split(' '):
      if token.isdigit():
        value = int(token)
        if 10 <= value % 100 < 20:
          res += token + 'th'
        else:
          res += token + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(value % 10, 'th')
      else:
        res += token
      res += ' '
    return res.strip()
  
  def make_station_appended_name(self, name):
    if name.endswith('station'):
      return name
    else:
      return name + ' station'
