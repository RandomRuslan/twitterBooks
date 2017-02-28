import os

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
		
	#to twit
	
	text = file.read()
	if len(text) == 0:
		if updateFile() == -1:
			return -1
	
	return

if __name__ == "__main__":
	if updateFile() == -1:
		print("end!")