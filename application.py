from flask import Flask, request, jsonify, session, render_template, redirect, url_for
import time
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import Stream
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

application = Flask(__name__)

host = ''
awsauth = AWS4Auth('', '', 'us-west-2', 'es')
es = Elasticsearch(
		hosts=[{'host': host, 'port': 443}],
		http_auth=awsauth,
		use_ssl=True,
		verify_certs=True,
		connection_class=RequestsHttpConnection
)

temp={}

@application.route("/notification", methods=['POST'])
def notification():
	typeOfMessage = request.headers.get('x-amz-sns-message-type')
	
	if typeOfMessage == 'SubscriptionConfirmation':
		jsonString=str(request.data)
		json1=json.loads(jsonString)
		res = es.index(index="confirmation", doc_type='sns', id='123', body=json1)

	if typeOfMessage == 'Notification':
		jsonString=str(request.data)
		json1=json.loads(jsonString)
		message=json1['Message']
		messageDict=json.loads(message)
		temp["text"]= messageDict['text']
		temp["name"]= messageDict['name']
		temp["latitude"]= messageDict['latitude']
		temp["longitude"]= messageDict['longitude']
		temp["sentiment"]= messageDict['sentiment']
		final = json.dumps(temp)
		res = es.index(index="tweets", doc_type='tweet', id=messageDict['id'], body=final)
		print(res['created'])

	return jsonify({'response' : '200'})

@application.route("/search", methods=['GET'])
def search():
	search_key = request.args.get('search_key')
	search_key = search_key.lower()
	latitude = []
	longitude = []
	text = []
	name = []
	sentiment = []

	res = es.search(index="tweets", body={"query": {"wildcard": {"text":'*'+search_key+'*'}}},size=400)
	hits = res['hits']['hits']
	if hits:
		for hit in hits:
			latitude.append(hit['_source']['latitude'])
			longitude.append(hit['_source']['longitude'])
			text.append(hit['_source']['text'])
			name.append(hit['_source']['name'])
			sentiment.append(hit['_source']['sentiment'])

	return jsonify({'latitude' : latitude, 'longitude' : longitude, 'text' : text, 'name' : name, 'sentiment' : sentiment})

@application.route("/")
def main():
	return render_template('index.html')

if __name__ == "__main__":
	application.debug = True
	application.run()