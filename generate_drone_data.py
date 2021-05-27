#!/usr/bin/env python3

import argparse
import csv
import os
from os import listdir
from os.path import isfile, join
import shutil

def main(locations, sensor,output_dir,n_sensors):
    location_files = [f for f in listdir(locations) if isfile(join(locations, f)) and f.endswith(".txt")]
    location_files.sort(key=lambda x : int(x[:-4]) )
    if n_sensors != None:
      location_files = location_files[:n_sensors] 
    sensor_files = [f for f in listdir(sensor) if isfile(join(sensor, f)) and f.endswith(".bin")]
    for f in location_files:
        sensor_name = f[:-4]
        location_dir = join(output_dir, sensor_name)
        try: 
            os.mkdir(location_dir) 
        except OSError as error: 
            print(error)  
            return 
        with open(join(locations,f)) as locations_csv:
            csv_reader = csv.reader(locations_csv, delimiter=' ')
            min_val = None
            max_val = None
            for row in csv_reader:
                time = float(row[2])
                if min_val == None or min_val > time:
                    min_val = time
                if max_val == None or max_val < time:
                    max_val = time
            assert(min_val != None and max_val != None)
        for s in sensor_files:
            sensor_time = float(s[:-4])
            if sensor_time >= min_val and sensor_time <= max_val:
                to_location = join(location_dir, s)
                from_location = join(sensor,s)
                shutil.copyfile(from_location, to_location)
        

  
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-L", dest = "locations", type=str, help="directory with all the location files 0.txt, 1.txt, ...")
    parser.add_argument("-S", dest = "sensor", type=str, help="directory with the base sensor data to be used for all the other sensors")
    parser.add_argument("-O", dest = "output_dir", type=str, help="directory that is going to contain the new sensor data")
    parser.add_argument("-N", dest = "total_sensors", type=int, help="Max number of sensors to process")
    args = parser.parse_args()
    main(args.locations,args.sensor,args.output_dir,args.total_sensors)

