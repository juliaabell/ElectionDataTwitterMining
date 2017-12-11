import tweepy
import csv 
import re
import geograpy

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
