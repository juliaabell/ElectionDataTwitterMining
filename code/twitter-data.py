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
    def x(self):
        if self._coords is not None:
            return self._coords[0]
        else:
            return None

    @property
    def y(self):
        if self._coords is not None:
            return self._coords[0]
        else:
            return None

class GeoStreamListener(tweepy.StreamListener):
    def __init__(self, tags, count):
        super(GeoStreamListener, self).__init__()
        self._tweet_collection = []
        self._tags = tags
        self._stream = None
        self._max_count = count

    def _geocode_tweet(self, tweet):

        # If the tweet contains geographic data just return it
        if tweet.place is not None:
            return tweet.place.bounding_box.corner()

        # Otherwise use geograpy + geopy to guess at location
        geograpy.places.PlaceContext(['United States'])
        e = geograpy.Extractor(text=tweet.text.encode('ascii', 'replace'))
        e.find_entities()
    
        geolocator = Nominatim()
        for place_name in e.places:
            try:
                location = geolocator.geocode(place_name)
                if location is not None:
                    return (location.latitude, location.longitude)
            except: 
                pass

        # give up
        return None

    def on_status(self, status):
        if len(self._tweet_collection) < self._max_count:
            location = self._geocode_tweet(status)
            if location is not None:
                tweet = Tweet(status.text, location)
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
    def __init__(self, partions, count):
        self._listeners = {k : GeoStreamListener(v, count) for k, v in partions.iteritems()}

    def start_streams(self, auth):
        for k in self._listeners:
            self._listeners[k].start_stream(auth)

    def disconnect_streams(self):
        for k in self._listeners:
            self._listeners[k].disconnect_stream()

    def collect_partions(self):
        return {k : v.collect_tweets() for k, v in self._listeners.iteritems()}

    def csv_dump(self, filename):
        with open(filename, 'wb') as tweet_file:
            writer = csv.writer(tweet_file)#, quoting=csv.QUOTE_NONNUMERIC)
            regex = re.compile(r'\s+')
            for name, tweets in self.collect_partions().iteritems():
                for tweet in tweets:
                    text = regex.sub(' ', tweet.text.encode('ascii', 'replace'))
                    writer.writerow([name, text, tweet.x, tweet.y])

    def stream_open(self):
        r = False
        for k in self._listeners:
            c = self._listeners[k].connected()
            r = r or c
        return r


consumer_key = 'qXFcavM2ZXwduSzUn5dlpE2XH'
consumer_secret = 'fhABJUgf0dJ5bCwvLtrnry5bKggRAEgqf71OQgLgQYq4ueDKOE'
access_token = '935886161217839104-p3rzIm3HfvhaE0THUQSf7hAfDVjIvJ2'
access_secret = '8E9tKooQeydsZwhuuFWuuoHJlS57oOyGShuhqy5323TgC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
 
partioner = GeoStreamPartioner({'Blue': ['#ManchesterDerby'], 'Red': ['#humanrightsday']}, 10)
partioner.start_streams(api.auth)

while(partioner.stream_open()):
    sleep(1)

partioner.csv_dump('tweet_dump.csv')
