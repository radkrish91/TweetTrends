# Tweet-Trends

Leveraged tweet data using the twitter API and displayed the same on a HeatMap using the Google Maps API while utilizing the ElasticSearch changefeed property to stream live data for a particular keyword using kafka and sns, thus reducing the overhead of polling the database constantly for new tweet data.

* Used the AWS SQS to create a processing queue for the Tweets that are delivered by the Twitter Streaming API.
* Used Amazon SNS service to update the status processing on each tweet so the UI can refresh.
* Integrated the third party cloud service API into the Tweet processing flow.

# Overview

Streaming

* Reads a stream of tweets from the Twitter Streaming API.
* After fetching a new tweet, check to see if it has geolocation info and is in English.
* Once the tweet validates these filters, send a message to AWS SQS for asynchronous processing on the text of the tweet

SQS and SNS

* Cretaed a SQS service using AWS console that will pick up geolocated tweets from [SQS Producer](https://github.com/radkrish91/TweetTrends/blob/master/producer_consumer/SQSProducer.py).
* Make a call to the sentiment API (Alchemy). This can return a positive, negative or neutral sentiment evaluation for the text of the submitted Tweet.
* As soon as the tweet is processed ([SQS Consumer](https://github.com/radkrish91/TweetTrends/blob/master/producer_consumer/SQSConsumer.py)) send a notification -using SNS- to an HTTP endpoint, that contains the information about the tweet.

[Backend](https://github.com/radkrish91/TweetTrends/blob/master/application.py)

* On receiving the notification, index this tweet in Elasticsearch and the sentiment of the tweet is preserved.
* The backend provides the functionality to the user to search for tweets that match a particular keyword.

[Frontend](https://github.com/radkrish91/TweetTrends/blob/master/templates/index.html)

* When a new tweet is indexed, visual indication on the frontend is provided in the form of a toast popup.
* The user can search the index via a dropdown where a predefined set of keywords are provided.
* The tweets that match the query are plotted on the map using markers.

# Architecture Diagram

![Architecture image](https://raw.githubusercontent.com/Vignesh6v/Tweet-Trends/master/static/ouIDUJT.png)
