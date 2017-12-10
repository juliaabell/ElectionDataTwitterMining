import tweepy
import csv
import re

import geograpy
from geopy.geocoders import Nominatim

from time import sleep
# from shapely.geometry.point import Point

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
                tweet = Tweet(status.text, status.place.bounding_box.corner)
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

    def collect_partions(self):
        return {k : v.collect_tweets() for k, v in self._listeners.iteritems()}

    def csv_dump(self, filename):
        print 'started geotaggin'
        with open(filename, 'wb') as tweet_file:
            writer = csv.writer(tweet_file)#, quoting=csv.QUOTE_NONNUMERIC)
            regex = re.compile(r'\s+')
            for name, tweets in self.collect_partions().iteritems():
                for tweet in tweets:
                    text = regex.sub(' ', tweet.text.encode('ascii', 'replace'))

                    if tweet.coords is None:
                        coords = self._geocode_tweet(text)
                        print 'coded', coords
                    else:
                        coords = tweet.coords
                        print 'place', coords

                    if coords is not None:
                        writer.writerow([name, text, coords[0], coords[1]])

    def stream_open(self):  
        r = False
        for k in self._listeners:
            c = self._listeners[k].connected()
            r = r or c
        return r

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

consumer_key = 'qXFcavM2ZXwduSzUn5dlpE2XH'
consumer_secret = 'fhABJUgf0dJ5bCwvLtrnry5bKggRAEgqf71OQgLgQYq4ueDKOE'
access_token = '935886161217839104-p3rzIm3HfvhaE0THUQSf7hAfDVjIvJ2'
access_secret = '8E9tKooQeydsZwhuuFWuuoHJlS57oOyGShuhqy5323TgC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
 
partioner = GeoStreamPartioner({'Blue': ['#ManchesterDerby'], 'Red': ['#humanrightsday']}, 10, Nominatim())

partioner.start_streams(api.auth)

while(partioner.stream_open()):
    sleep(1)

partioner.csv_dump('tweet_dump.csv')
