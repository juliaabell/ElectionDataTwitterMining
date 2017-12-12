# Final project submission


Use this project for interacting with your group. I suggest you to keep the folders updated (especially the one containing). I also suggest to use the `issue` feature in github for communicating with your teammates since that way it will be easier to debug your code.

For each deadline I will count as submitted the files uploaded in the corresponding folder.

Use:

- the `intro_presentation` folder for your initial presentation introducing your project (**deadline 11/19**)

- the `documentation` folder for your full documentation (**deadline 11/26**). If you like the Markdown syntax you can modify this README.md file for providing the documentation of your project. A tutorial can be found [here](https://www.markdowntutorial.com)

- the `code` folder upload the project's code (**deadline 12/11**)

- the `final_presentation` folder upload the final presentation at least one day before the actual discussion (date to arrange with the instructor)

# Political Data Mining Code Documentation

## Introduction

Twitter is a widely used social media website that gives a platform to users across the world to share their own opinions about events, trends, and connect with people globally. Twitter is also a powerful tool in the observation of both global and local trends through the use of hashtags and geotagging. Geotagging a tweet is optional for each user, if the tweet is geotagged, it is given latitude and longitude coordinates specific to the tagged location. Geotagged data can be used to show geographic trends that show how many people are talking about a certain topic within a certain area. However, geotagging is optional, and some tweets do not have easily readable geographic coordinates.

Our project seeks to use the python module _tweepy_ to access the Twitter API and find the geographic dispersion of tweets using partisan political hashtags. Since partisan sentiment is often concentrated in different geographic regions, producing a visualization of the dispersion of tweets using each hashtag could prove intersting. In addition, our code will seek to geotag those messages that are not geotagged by the user.

## tweepy Module

The tweepy module is used to access the twitter API and begin the process of data mining. This module is important to our code because it will provide access to the tweets necessary to perform our analysis. We will use the _tweepy.API_ class, which serves as a wrapper to the twitter API and gives us access to the desired data stored within twitter. 

### API Authorization

Before being able to search through the tweets that we want, we must first get authorized access to the twitter API for our users. The _OAuth_ function of tweepy allows us to get access to the code. We have to register the module to twitter and then use the consumer key given to us by twitter to use the tweepy module to allow our module to operate and collect data. After receiving a token, we then have access to the API and data stored within twitter. To learn more about API authorization in tweepy follow this [link](http://tweepy.readthedocs.io/en/v3.5.0/auth_tutorial.html)

### tweepy Stream

The tweepy module has the capability to stream tweets and produce a JSON dataset that includes several parameters. This can be used to return data for tweets including the partisan hashtags provided as input. The data returned through tweepy stream will be used in the rest of our analysis. While just a regular stream will return all available tweets for a certain time, we need something more specific for our hashtags. The tweepy module provides a search function which will help us narrow down tweets that contain one of the hashtags within their text. Theis requires an input of the string (hashtag) we are looking for, as well as a specification of how many tweets we should return. This will be how our initial dataset will be created, the next step is geocoding ungeotagged tweets. For a more easily readable dataset, the JSON is converted into a .csv file.

A list of hashtags for each party have been used to collect the tweets, each stream will look for tweets using these hashtags, and then it will create a category for each tweet, Red or Blue. The Red or Blue categorization, along with the physical text of the tweet, are added to the .csv file along with fields for latitude and longitude coordinates. 

## Geocoding and Visualization

### Using Tweet Text for Geocoding

A tweet is geotagged only when a user allows it to be, therefore many tweets do not have latitude and longitude coordinates already. After we have retrieved tweets using both functions, the dataset will have to geotag as many of the untagged tweets as possible. Fortunately, it is possible to analyze individual tweets within the JSON dataset created by using the text function of tweepy, which returns the text of the tweet as a string object. Our code will use the text of each tweet and create a place and coordinate dictionary that will search tweets for text that indicates a location, and then populating a coordinate field with lat lon coordinates that correspond to the written location within the tweet. This will help to create more robust geospatial datasets derived from twitter and increase the sample size of our analysis of partisan hashtags.

To realize this function, we used the [**geograpy**](https://pypi.python.org/pypi/geograpy) library, which uses NLTK place name tokens to parse a string and create a list of all things that correspond to place in the script. The next step is using these placenames to geocode the tweets to specific coordinates. To do this we used [**geopy**](https://pypi.python.org/pypi/geopy) to give us access to the Nomanatim geocoder provided by Open Street Map. For each tweet, lat/lon coordinates will be added to the .csv file.

### Visualization of Data

The visualization portion of this project will edit the .csv file, turning the partitioned tweets into two shapefiles, one for right-leaning hashtags and the other for left-leaning hashtags. In order to display these shapefiles, a count is taken for the amount of states in each boundary. The GeoPandas library is used to make chloropleth maps that show the concentration of partisan tweets within each state. 

## UML Diagram and Implementation

![UML Diagram](/documentation/uml.png)

Tweepy is a python library used for accessing the twitter API. This will allow us to scrape the information that we want from Twitter. From  Tweepy, we will use StreamListener which will allow us to access the tweets and download them.

Tweet will contain the tweets that have been downloaded from twitter via the Tweepy module. Each tweet will have a status which is the string/words in the tweet (including the hashtag, which is what we are most interested in), as well as geographic information about where the tweet originated. 

GeoStreamListener is composed of these tweets and allows us to obtain the geographic location of where the tweet was created to create a geodataset of tweets. 

GeoTweetCollection is composed of the partitioned tweets and the tweets that have been geotagged so we can determine where they were created. Any tweets that we haved ownloaded that cannot be tagged will be dropped from this dataset as we need location for this project.

GeoTweetView will take the location of the selected tweets and display them in their correct location on a map of the U.S. This map will be partitioned by state, so we can easily see which state each tweet came from. This graphic can be used to compare the political affilition of each state with the tweets that are being tweeted by its citizens. 


## Project Input & Output

As a whole our project seeks to analyze partisan sentiment on twitter by using the geospatial data that is retrievable through the twitter API. In order to create our final product, we require some input:

* Twitter API Authorization token
* List of hashtags to be used: Blue(#lovetrumpshate, #hillaryclinton, #obama, #resist, #trumprussia, #impeachtrump, #trumpconspired,
#TraitorTrump), Red(#makeamericagreatagain, #trump, #maga, #republican, #liberaltears, #killaryforprison, #hillaryforprison, #buildthewall)

With these two inputs, we are able to create our output:

* A corrected geodataset of tweets in .csv form called political_tweets.csv (All tweets that could not be tagged will be deleted).
* Geovisualization of data using shapely, fiona, and geopandas


