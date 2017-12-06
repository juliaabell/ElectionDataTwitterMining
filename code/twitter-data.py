import tweepy

from time import sleep

class GeoStreamListener(tweepy.StreamListener):
    def __init__(self, tags, count):
        super(GeoStreamListener, self).__init__()
        self._tweet_collection = []
        self._tags = tags
        self._stream = None
        self._max_count = count

    def on_status(self, status):
        if len(self._tweet_collection) < self._max_count:
            print 'tweet for', self._tags
            self._tweet_collection.append(status.text)
            if len(self._tweet_collection) >= self._max_count:
                self.disconnect_stream()
        else:
            self.disconnect_stream()

    def collect_tweets(self):
        return self._tweet_collection

    def start_stream(self, auth):
        if self._stream is not None:
            raise Exception('Stream already exists for this listener object!')
        print 'started stream', self._tags
        self._stream = tweepy.Stream(auth = auth, listener = self)
        self._stream.filter(track=self._tags, async=True)

    def disconnect_stream(self):
        if self._stream is None:
            raise Exception('No stream exists for this listener object!')
        print 'closed stream', self._tags
        self._stream.disconnect()
        self._stream = None

    def connected(self):
        print self._stream is not None, self._tags
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
 
partioner = GeoStreamPartioner({'Blue': ['#democrats','Clinton Foundation'], 'Red': ['#MAGA']}, 1000)
partioner.start_streams(api.auth)

while(partioner.stream_open()):
    print 'waiting'
    sleep(1)

print partioner.collect_partions()
