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

The tweepy module is used to access the twitter API and begin the process of data mining.
