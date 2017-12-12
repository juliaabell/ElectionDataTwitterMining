from twitterdata import GeoTweetView

view = GeoTweetView('../political_tweets.csv', '../Election_map.shp', 'red.shp', 'blue.shp')
view.convert_csv()
view.populate_indices()
view.finalize_tweets()
view.display_tweets()
