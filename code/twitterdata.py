import tweepy
import csv 
import re
import geograpy
from shapely.geometry import Point, mapping, Polygon
import fiona
from fiona.crs import from_epsg
import pandas
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
from rtree import index

class Tweet():
    def __str__(self):
        return str(self.__dict__)

    def __init__(self, text, coords):
    	self._text   = text
        self._coords = coords 

    @property
    def text(self):
        return self._text

    @property
    def coords(self):
      return self._coords

class GeoStreamListener(tweepy.StreamListener):
    def __init__(self, tags, count):
        super(GeoStreamListener, self).__init__()
        self._tweet_collection = []
        self._tags = tags
        self._stream = None
        self._max_count = count

    def on_status(self, status):
        if len(self._tweet_collection) < self._max_count:
            if status.place is not None:
                print 'found geotagged tweet'
                tweet = Tweet(status.text, status.place.bounding_box.corner())
            else:
                tweet = Tweet(status.text, None)

            self._tweet_collection.append(tweet)
            if len(self._tweet_collection) >= self._max_count:
                self.disconnect_stream()

        else:
            self.disconnect_stream()

    def collect_tweets(self):
        return self._tweet_collection

    def start_stream(self, auth):
        if self._stream is not None:
            raise Exception('Stream already exists for this listener object!')
        self._stream = tweepy.Stream(auth = auth, listener = self)
        self._stream.filter(track=self._tags, async=True)

    def disconnect_stream(self):
        if self._stream is None:
            raise Exception('No stream exists for this listener object!')
        self._stream.disconnect()
        self._stream = None

    def connected(self):
        return self._stream is not None


class GeoStreamPartioner():

    # partions :: Dict String [String]
    def __init__(self, partions, count, geolocator):
        self._listeners = {k : GeoStreamListener(v, count) for k, v in partions.iteritems()}
        self._geolocator = geolocator

    def start_streams(self, auth):
        for k in self._listeners:
            self._listeners[k].start_stream(auth)

    def disconnect_streams(self):
        for k in self._listeners:
            self._listeners[k].disconnect_stream()

    def stream_open(self):  
        r = False
        for k in self._listeners:
            c = self._listeners[k].connected()
            r = r or c
        return r

    # Geocoding is done when the user collects the partions because the process
    # is to slow to do while connected to the twitter API. Attempting to do that
    # casused the twitter API to time out.
    def collect_partions(self):
        coded_partions = {}
        for name,listener in self._listeners.iteritems():

            partion = []
            regex = re.compile(r'\s+')
            for tweet in listener.collect_tweets():
                text = regex.sub(' ', tweet.text.encode('ascii', 'replace'))
                if tweet.coords is None:
                    coords = self._geocode_tweet(text)
                else:
                    corrds = tweet.coords
                if coords is not None:
                    partion.append(Tweet(text, coords))

            coded_partions[name] = partion

        return coded_partions

    def csv_dump(self, filename):
        with open(filename, 'wb') as tweet_file:
            writer = csv.writer(tweet_file)#, quoting=csv.QUOTE_NONNUMERIC)
            for name, tweets in self.collect_partions().iteritems():
                for tweet in tweets:
                    writer.writerow([name, tweet.text, tweet.coords[0], tweet.coords[1]])

    def _geocode_tweet(self, text):
        # Try to use geograpy + geopy to guess at location
        geograpy.places.PlaceContext(['United States'])
        e = geograpy.Extractor(text=text)
        e.find_entities()

        for place_name in e.places:
            try:
                location = self._geolocator.geocode(place_name)
                if location is not None:
                    return (location.latitude, location.longitude)
            except: 
                pass

        # give up
        return None

class GeoTweetView():

    def __init__(self, partioned_csv, state_file, red_shp, blue_shp):
        self.partioned_csv = partioned_csv
        self.state_file = state_file
        self.red_shp = red_shp
        self.blue_shp = blue_shp
        self.red_idx = index.Index()
        self.blue_idx = index.Index()

    #converts csv file into 2 shapefiles for Blue tweets and red tweets
    def convert_csv(self):
         newschema = {'geometry': 'Point', 'properties': {'text': 'str', 'party':'str'}}
         with fiona.open(self.red_shp, 'w', driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as red:
             with fiona.open(self.blue_shp, 'w', driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as blue:
                 with open(self.partioned_csv, 'rb') as f:
                     reader = csv.reader(f)#csv.DictReader(f)
                     for row in reader:
                         if row[0] == 'Red':
                             point = Point(float(row[2]), float(row[3]))
                             red.write({'properties': {'text': row[1], 'party': row[0]},'geometry': mapping(point)})
                         elif row[0] == 'Blue':
                             point = Point(float(row[2]), float(row[3]))
                             blue.write({'properties': {'text': row[1], 'party': row[0]},'geometry': mapping(point)})
    
    #This will create an Rtree index of the geocoded tweets
    def populate_indices(self):
        count = 0
        with fiona.open(self.red_shp, 'r') as shp_input:
            for point in shp_input:
                self.red_idx.insert(count, point['geometry']['coordinates'])
                count = count + 1
        count2 = 0
        with fiona.open(self.blue_shp, 'r') as blue_input:
            for point in blue_input:
                self.blue_idx.insert(count2, point['geometry']['coordinates'])
    
    #This finalizes the data structure of the shapefiles in order to display the data in a map
    def finalize_tweets(self):
        with fiona.open(self.state_file, 'r') as states:
            newschema = states.schema.copy()
            newschema['properties']['blue_count'] = 'float'
            newschema['properties']['red_count'] = 'float'

            with fiona.open(self.state_file + '.new', 'w', driver="ESRI Shapefile", schema = newschema, crs = from_epsg(4296)) as new_state:
                    for state in states:

                        min_x = min(map(lambda c: c[0], get_list(state['geometry']['coordinates'])))
                        min_y = min(map(lambda c: c[1], get_list(state['geometry']['coordinates'])))

                        max_x = max(map(lambda c: c[0], get_list(state['geometry']['coordinates'])))
                        max_y = max(map(lambda c: c[1], get_list(state['geometry']['coordinates'])))

                        state['properties']['red_count'] = self.red_idx.count([min_x,min_y,max_x,max_y])
                        state['properties']['blue_count'] = self.blue_idx.count([min_x,min_y,max_x,max_y])
                        new_state.write(state)
                        
        
    def display_tweets(self):
        query_box = [-168.6,16.4,-66.5,71.5]
        stateplot = gpd.read_file(self.state_file)
        stateplot.plot( cmap = 'Reds', scheme = 'quantiles')
        stateplot.plot( cmap = 'Blues', scheme = 'quantiles')
        plt.show()

def get_list(lst):
    if not isinstance(lst, list):
        return None
    elif get_list(lst[0]) is not None:
        return get_list(lst[0])
    else:
        return lst
