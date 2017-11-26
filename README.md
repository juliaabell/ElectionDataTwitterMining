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

### tweepy Stream and tweepy.search

The tweepy module has the capability to stream tweets and produce a JSON dataset that includes several parameters. This can be used to return data for tweets including the partisan hashtags provided as input. The data returned through tweepy stream will be used in the rest of our analysis. While just a regular stream will return all available tweets for a certain time, we need something more specific for our hashtags. The tweepy module provides a search function which will help us narrow down tweets that contain one of the hashtags within their text. The search function requires an input of the string (hashtag) we are looking for, as well as a specification of how many tweets we should return. This will be how our initial dataset will be created, the next step is geocoding ungeotagged tweets.

### tweepy.text and Geotagging Function

A tweet is geotagged only when a user allows it to be, therefore many tweets do not have latitude and longitude coordinates already. After we have retrieved tweets using both functions, the dataset will have to geotag as many of the untagged tweets as possible. Fortunately, it is possible to analyze individual tweets within the JSON dataset created by using the text function of tweepy, which returns the text of the tweet as a string object. Our code will use the text of each tweet and create a place and coordinate dictionary that will search tweets for text that indicates a location, and then populating a coordinate field with lat lon coordinates that correspond to the written location within the tweet. This will help to create more robust geospatial datasets derived from twitter and increase the sample size of our analysis of partisan hashtags.

### Geovisualization of Data

Our code will aim to create a visualization of the data in the form of a map showing the dispersion of partisan tweets by geographic location. These maps will be created using the basemap functionality of matplotlib, and will be an important utilization of the geographic data that has been created in the other parts of our code.
