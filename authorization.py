import tweepy

class GeoStreamListener(tweepy.StreamListener):
    hashtags = {'red': ["#Hillaryforprison", "#PresidentTrump", "#MakeAmericaGreatAgain", "#MAGA"], 'blue': ["#LoveTrumpsHate", "#NotMyPresident", "#PresidentClinton"]}
    def on_status(self, status):
        print(status.text)
    
    def collect_tweets(self):
        return None #Will be revised later

consumer_key = 'qXFcavM2ZXwduSzUn5dlpE2XH'
consumer_secret = 'fhABJUgf0dJ5bCwvLtrnry5bKggRAEgqf71OQgLgQYq4ueDKOE'
access_token = '935886161217839104-p3rzIm3HfvhaE0THUQSf7hAfDVjIvJ2'
access_secret = '8E9tKooQeydsZwhuuFWuuoHJlS57oOyGShuhqy5323TgC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

myListener = GeoStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener = myListener)

myStream.filter(track=['MAGA'])
