import time
from HTMLParser import HTMLParser
import tweepy
import jsonify
import json
from time import strftime,gmtime,time
import urllib2
import hmac
import hashlib
import base64
import string

from alchemyapi import AlchemyAPI
alchemyapi = AlchemyAPI()

import time
import threading
import boto3

temp = {}
mess = {}

def publishAmazonSnsMsg(message):
	client = boto3.client('sns')
	#final = json.dumps({"default": "my default", "sqs": json.dumps({"id": message["id"]}, {"name": message["name"]}, {"latitude" : message["latitude"]}, {"longitude" : message["longitude"]}, {"sentiment": message["sentiment"]})})
	json_message = json.dumps({"default":json.dumps(message)})
	response = client.publish(
	    TopicArn='',
	    MessageStructure='json',
	    Message=json_message
	)
	print response['MessageId']

def subscribeSnsEndpoint():
	client = boto3.client('sns')
	response = client.subscribe(
	    TopicArn='',
	    Protocol='http',
	    Endpoint=''
	)
	print response['SubscriptionArn']

if __name__ == '__main__':
	#subscribeSnsEndpoint()
	while True:
		sqs = boto3.resource('sqs')
		queue = sqs.get_queue_by_name(QueueName='tweets')

		for message in queue.receive_messages(MessageAttributeNames=['All']):
			try:
				temp["text"] = message.body
				response = alchemyapi.sentiment("text", temp["text"])
				if message.message_attributes is not None:
					temp["id"]= message.message_attributes.get('id').get('StringValue')
					temp["name"]= message.message_attributes.get('name').get('StringValue')
					temp["latitude"]= message.message_attributes.get('latitude').get('StringValue')
					temp["longitude"]= message.message_attributes.get('longitude').get('StringValue')
				temp["sentiment"] = response["docSentiment"]["type"]

			except KeyError:
				message.delete()	

			publishAmazonSnsMsg(temp)
	    	message.delete()