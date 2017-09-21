import os
import requests
import tweepy
from datetime import datetime, timedelta

def lastSpace(s):
	for i in range(len(s)):
		if s[len(s)-i-1] in [" ", "\f", "\n", "\r", "\t", "\v"]:
			return len(s)-i-1
	return -1

def updateFile():		#fill cash if it's empty	
	print("updateFile")
	fullFile = open("fullText.txt", "r")
	blockSize = 140*10
	block = ""
	text = fullFile.read(blockSize+1)
	
	if len(text) == 0:
		fullFile.close()
		cashFile = open("cashText.txt", "w")
		cashFile.write(text)
		cashFile.close()
		return -1
	
	for i in range(10):
		if len(text) < 141:
			block = block + "[" + str(len(text)) + "]"  + text
			text = ""
			break
		tweet = text[:141]
		text = tweet[lastSpace(tweet)+1:] + text[141:]
		tweet = tweet[:lastSpace(tweet)]
		block = block + "[" + str(len(tweet)) + "]"  + tweet
	
	
	cashFile = open("cashText.txt", "w")
	cashFile.write(block)
	cashFile.close()
	
	tmpFile = open("tmp.txt", "w")
	tmpFile.write(text)
	while True:		
		text = fullFile.read(blockSize)
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

	with open("cashText.txt", "r") as f:
	    text = f.read()
	    #tweet = file.read(140)
	
	if(len(text) == 0): # cashText is empty
		if updateFile() == -1:
			return -1
		return toTweet(api, lastTweet)
	bracket = text.find("]")
	lenTweet = int(text[text.find("[")+1:bracket])
	tweet = text[bracket+1:bracket+1+lenTweet]
	text = text[bracket+1+lenTweet:]
	
	if(tweet == lastTweet.text):	#check: tweet was here
		if len(text) < 140:
			tweet = text[bracket+1:]
			text = ''
		else:
			lenTweet = int(text[text.find("[")+1:bracket])
			tweet = text[bracket+1:bracket+1+lenTweet]
			text = text[bracket+1+lenTweet:]	    
	api.update_status(tweet) #to tweet
	
	if len(text) == 0:
		if updateFile() == -1:
			return -1
	else:
		file = open("cashText.txt", "w")
		file.write(text)
		file.close()
	return 0

def main():
	#get keys and tokens
	with open("const.txt", "r") as f:
	   CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = f.read().split()
	
	#connect with twitter
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	tweets = api.user_timeline()
	lastTweet = tweets[0]
	
	return toTweet(api, lastTweet)

	#get real time
	"""
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
		return toTweet(api, lastTweet)
	"""
	
if __name__ == "__main__":
	if main() == -1:
		with open("error.txt", "w") as f:
			f.write("Error!")
	

	
	
	
	
	