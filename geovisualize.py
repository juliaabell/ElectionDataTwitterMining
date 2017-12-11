import os.path
from shapely.geometry import Polygon, MultiPolygon, Point, mapping
from descartes.patch import PolygonPatch

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

import pyproj
import fiona
import fiona.crs

import csv

#Makes two fiona shapefiles from the csv dataset, separating them by party
def convert_csv(data_csv, red_file, blue_file):
    newschema = {'geometry': 'Point', 'properties': {'text': 'str', 'party':'str'}}
    with fiona.open(red_file, 'w', driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as red:
        with fiona.open(blue_file, 'w', driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as blue:
            with open(data_csv, 'rb') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row[0] == 'Red':
                        point = Point(float(row[2]), float(row[3]))
                        red.write({'properties': {'text': row[1], 'party': row[0]},'geometry': mapping(point)})
                    elif row[0] == 'Blue':
                        point = Point(float(row[2]), float(row[3]))
                        blue.write({'properties': {'text': row[1], 'party': row[0]},'geometry': mapping(point)})


#This collection of functions will be able to visualize our tweet datasets and compare them to election results
def populate_index(idx, name_file_in):
    count = 0
    with fiona.open(name_file_in, 'r') as shp_input:
        for point in shp_input:
            idx.insert(count, Point(point['geometry']['coordinates'][0].bounds))
            count = count + 1

#This function cleans the fiona shapefile and creates the count file                                   
def finalize_tweets(state_set, red_set, blue_set, blue_idx, red_idx):
    with fiona.open(state_set, 'r') as states:
        newschema = states.schema.copy()
        newschema['properties']['count'] = 'float'
        with fiona.open(driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as red:
            for state in red:
                state['properties']['count'] = idx.count(Polygon(state['geometry']['coordinates'][0].bounds))
            with fiona.open(driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as blue:
                for state in blue:
                    state['properties']['count'] = idx.count(Polygon(state['geometry']['coordinates'][0].bounds))
                 
                 
        
    
    
