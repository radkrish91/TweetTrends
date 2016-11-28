import time
from HTMLParser import HTMLParser
import tweepy
import jsonify
import json
from tweepy.streaming import StreamListener
from tweepy import Stream

import time
import threading
import boto3

temp={}

class MyListener(StreamListener):

    def on_error(self, status):
		print(status)

    def on_data(self, data):
		decoded = json.loads(data)
		if decoded.get('coordinates',None) is not None:
			coordinates = decoded.get('coordinates','').get('coordinates','')
			temp["text"]= remove_non_ascii_1(decoded['text'])
			temp["id"]= str(decoded['id'])
			temp["name"]= decoded['user']['screen_name']
			temp["latitude"]= str(decoded['coordinates']['coordinates'][1])
			temp["longitude"]= str(decoded['coordinates']['coordinates'][0])
			temp["search_key"]= 'trump'
			print temp
			queue.send_message(MessageBody=temp["text"], MessageAttributes={
			    'id': {
			    	'StringValue' : temp["id"],
			    	'DataType' : 'String'
			    },
			    'name': {
			    	'StringValue' : temp["name"],
			    	'DataType' : 'String'
			    },
			    'latitude': {
			    	'StringValue' : temp["latitude"],
			    	'DataType' : 'String'
			    },
			    'longitude': {
			    	'StringValue' : temp["longitude"],
			    	'DataType' : 'String'
			    }
			})
			
		return True	

def remove_non_ascii_1(text):
	return ''.join([i if ord(i) < 128 else '' for i in text])

if __name__ == '__main__':
	auth = tweepy.OAuthHandler("", "")
	auth.set_access_token("", "")
	
	sqs = boto3.resource('sqs')

	# Get the queue. This returns an SQS.Queue instance
	queue = sqs.get_queue_by_name(QueueName='tweets')

	# You can now access identifiers and attributes
	print(queue.url)
	print(queue.attributes.get('DelaySeconds'))

	api = tweepy.API(auth)
	#track = ['obama', 'trump', 'manchester', 'pogba', 'clinton']
	start_time = time.time()
	twitter_stream = Stream(auth, MyListener())
	twitter_stream.filter(languages=["en"], track=['hillary', 'trump', 'patriots', 'clinton', 'giants', 'jets', 'football', 'mufc', 'rosberg', 'coyg'])
