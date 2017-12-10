import geograpy
from geopy.geocoders import Bing
import json

def geocode_tweets(tweet, fil):
    geograpy.places.PlaceContext(['United States'])
    pc.set_countries()
    e = geograpy.Extractor(text=tweet)
    e.find_entities()
    place_name = e.places[0]
    geolocator = Nomanatim()
    location = geolocator.geocode(place_name)
    with open(fil, 'r+') as tweet_file:
        data = json.load(tweet_file)
        data['coordinates']['coordinates'] = location.longitude, location.latitude
        
