import os
import requests
import tweepy
from datetime import datetime, timedelta
def updateFile():		#fill cash if it's empty	
	print("updateFile")
	fullFile = open("fullText.txt", "r")
	block = 140*10
	text = fullFile.read(block)
	if len(text) == 0:
		fullFile.close()
		cashFile = open("cashText.txt", "w")
		cashFile.write(text)
		cashFile.close()
		return -1

	cashFile = open("cashText.txt", "w")
	cashFile.write(text)
	cashFile.close()
	
	tmpFile = open("tmp.txt", "w")
	while True:		
		text = fullFile.read(block)
		if len(text) == 0:
			break
		tmpFile.write(text)
	fullFile.close()
	tmpFile.close()
	
	os.remove("fullText.txt")
	os.rename("tmp.txt", "fullText.txt")	
	return 0 

def toTweet(api, lastTweet):	#to tweet
	print("tweet")
	file = open("cashText.txt", "r")
	tweet = file.read(140)
	text = file.read()
	file.close()
	
	#check: tweet was here or cashText is empty
	if(tweet == lastTweet.text or len(tweet) == 0):
		if len(text) == 0:
			if updateFile() == -1:
				file.close()
				return -1
			return toTweet(api, lastTweet)
		elif len(text) < 140:
			tweet = text
			text = ''
		else:
			tweet = text[:140]
			text = text[140:]
	    
	api.update_status(tweet) #to tweet
	
	if len(text) == 0:
		if updateFile() == -1:
			return -1
	else:
		file = open("cashText.txt", "w")
		file.write(text)
		file.close()
	return

if __name__ == "__main__":

	#get keys and tokens
	f = open("const.txt", "r")
	CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, TIME_KEY = f.read().split()
	f.close()
	
	#connect with twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweets = api.user_timeline()
	lastTweet = tweets[0]
	
	#get real time
	url = "http://api.timezonedb.com/v2/get-time-zone"
	params = {
		'key' : TIME_KEY,
		'format' : 'json',
		'by' : 'zone',
		'zone' : 'Europe/London'
	}
	nowTime = requests.get(url, params=params).json()
	nowTime = datetime.strptime(nowTime["formatted"], "%Y-%m-%d %H:%M:%S")
	if(nowTime - lastTweet.created_at > timedelta(hours=5)):
		if toTweet(api, lastTweet) == -1:
			print("The End!")

	
	
	
	
	