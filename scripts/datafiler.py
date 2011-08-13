import csv
import sys

# A class that reads in GTFS data and produces a CSV file of stations, with
# their MTA IDs, display names, latitudes and longitues, and lists of routes.
class DataFiler:
  
  IN_STOPS_FILE_NAME = 'stops.txt'
  IN_TRIPS_FILE_NAME = 'trips.txt'
  IN_STOP_TIMES_FILE_NAME = 'stop_times.txt'
  
  def __init__(self, in_path, out_file, err):
    self.in_path = in_path
    self.out_file = out_file
    self.err = err
    self.stations = {}
    self.stops = {}
    self.trips = {} # a dictionary from trip ids to route ids
  
  def file(self):
    self.read_stops()
    self.read_trips()
    self.read_stop_times()
    self.write_stations()
  
  def read_stops(self):
    f = open(self.in_path + DataFiler.IN_STOPS_FILE_NAME)
    f.readline() # reading past header line
    line = f.readline()
    while line != '':
      data = line.split(',')
      if len(data) < 4:
        line = f.readline()
        continue
      mta_id = data[0]
      parent_id = data[9].strip()
      if parent_id == '':
        # this is a station
        display_name = data[2]
        lat = data[4]
        lng = data[5]
        station = Stop(mta_id, display_name, lat, lng, None)
        self.stations[mta_id] = station
      else:
        # this is a stop within a station
        stop = Stop(mta_id, None, None, None, parent_id)
        self.stops[mta_id] = stop
      line = f.readline()
    f.close()
  
  def read_trips(self):
    f = open(self.in_path + DataFiler.IN_TRIPS_FILE_NAME)
    f.readline() # reading past header line
    line = f.readline()
    while line != '':
      data = line.split(',')
      if len(data) < 3:
        line = f.readline()
        continue
      self.trips[data[2]] = data[0]
      line = f.readline()
    f.close()
  
  def read_stop_times(self):
    f = open(self.in_path + DataFiler.IN_STOP_TIMES_FILE_NAME)
    f.readline() # reading past header line
    line = f.readline()
    while line != '':
      data = line.split(',')
      if len(data) < 5:
        line = f.readline()
        continue
      route_id = self.trips[data[0]]
      parent_id = self.stops[data[3]].parent_id
      station = self.stations[parent_id]
      station.routes.add(route_id)
      line = f.readline()
    f.close()
  
  def write_stations(self):
    f = open(self.out_file, 'w')
    for station_id in self.stations:
      station = self.stations[station_id]
      routelist = ''
      for route_id in station.routes:
        routelist += '/' + route_id
      line = '%s,%s,%s,%s,%s\n' % (station.mta_id, station.display_name, \
          station.lat, station.lng, routelist[1:])
      f.write(line)
    f.close()

class Stop:
  def __init__(self, mta_id, display_name, lat, lng, parent_id):
    self.mta_id = mta_id
    self.display_name = display_name
    self.lat = lat
    self.lng = lng
    self.parent_id = parent_id
    self.routes = set()

def main():
  if len(sys.argv) != 3:
    sys.stderr.write('dataparser requires two arguments\n')
    return
  in_path = sys.argv[1]
  out_file = sys.argv[2]
  df = DataFiler(in_path, out_file, sys.stderr.write)
  df.file()

if __name__ == '__main__':
  main()
