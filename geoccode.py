import geograpy

def extract_location(text):
    e = geograpy.Extractor(text)
    e.find_entities()
    return e.places

def geocode_tweets(text):
    e = geograpy.Extractor(text)
    e.find_entities()
    e.places[0]
    
    