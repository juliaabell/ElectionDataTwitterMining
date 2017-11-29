import tweepy
from tweepy import OAuthHandler

consumer_key = 'qXFcavM2ZXwduSzUn5dlpE2XH'
consumer_secret = 'fhABJUgf0dJ5bCwvLtrnry5bKggRAEgqf71OQgLgQYq4ueDKOE'
access_token = '935886161217839104-p3rzIm3HfvhaE0THUQSf7hAfDVjIvJ2'
access_secret = '8E9tKooQeydsZwhuuFWuuoHJlS57oOyGShuhqy5323TgC'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)