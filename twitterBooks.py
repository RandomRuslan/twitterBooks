import os
import requests
import tweepy
from datetime import datetime, timedelta
def updateFile():		#fill cash if it's empty
	fullFile = open("fullText.txt", "r")
	block = 5*1
	text = fullFile.read(block)
	if len(text) == 0:
		fullFile.close()
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
	
def twitter():	#to tweet
	file = open("cashText.txt", "+")
	text = file.read(140)
	
	#check: tweet was here
		
	#to tweet    api.update_status(tweet,id_reply)
	
	text = file.read()
	if len(text) == 0:
		if updateFile() == -1:
			return -1
	
	return

if __name__ == "__main__":
	"""
	if updateFile() == -1:
		print("end!")
	"""
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
		print(nowTime, lastTweet.created_at)
		
		
	
	

	
	
	
	
	
	