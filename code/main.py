from twitterdata import GeoStreamPartioner
from geopy.geocoders import Nominatim
from time import sleep
import tweepy
import sys

# Call as With:
# python main.py count csv

consumer_key = 'qXFcavM2ZXwduSzUn5dlpE2XH'
consumer_secret = 'fhABJUgf0dJ5bCwvLtrnry5bKggRAEgqf71OQgLgQYq4ueDKOE'
access_token = '935886161217839104-p3rzIm3HfvhaE0THUQSf7hAfDVjIvJ2'
access_secret = '8E9tKooQeydsZwhuuFWuuoHJlS57oOyGShuhqy5323TgC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)
 
with open('blue_tags.txt') as f:
    blue_tags = [l.strip() for l in f.readlines()]

with open('red_tags.txt') as f:
    red_tags = [l.strip() for l in f.readlines()]

partioner = GeoStreamPartioner({'Blue': blue_tags,
                                'Red': red_tags}, int(sys.argv[1]), Nominatim())

partioner.start_streams(api.auth)

while(partioner.stream_open()):
    sleep(1)

partioner.csv_dump(sys.argv[2])
