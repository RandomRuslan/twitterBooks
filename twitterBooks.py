import os
import requests
import tweepy, webbrowser
from datetime import datetime, date, time
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
	
def twitter():
	file = open("cashText.txt", "+")
	text = file.read(140)
	
	#check: twit was here
		
	#to twit    api.update_status(twit,id_reply)
	
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
	f = open("tokens.txt", "r")
	CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET = f.read().split()
	f.close()
	
	auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
	api = tweepy.API(auth)

	public_tweets = api.user_timeline()
	lastTweet = public_tweets[0]
	
	
	twi = lastTweet.created_at
	now = datetime.now()
	t = datetime(1995, 3, 6, 10, 10, 10)
	five = time(hour=5)
	print(twi)
	print(now)
	print(t)
	print(time(t))
	print(five)
	#print(t-five)
	
	
	
	
	
	