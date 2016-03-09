import imaplib2,smtplib,time,email
from threading import *
from imageProcessing import *
import atexit
myEmail = "wordswithfriendssolver@gmail.com"

def loginSMTP(password):
	'''
	Logs into the SMTP server, creating an smtpObj for sending emails.
	'''
	global smtpObj
	smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
	assert smtpObj.ehlo()[0] == 250
	smtpObj.starttls()
	smtpObj.login(myEmail,password)
	print "SMTP done!"

def loginIMAP(password):
	'''
	Logs into the SMTP server, creating an smtpObj for sending emails. It also starts an IDLE process.
	'''
	global idler,imapObj
	imapObj = imaplib2.IMAP4_SSL("imap.googlemail.com")
	imapObj.login(myEmail,password)
	imapObj.select("INBOX")
	idler = Idler(imapObj)
	idler.start()
	print "IMAP done!"

def login(password):
	'''
	Logs into both processes.
	'''
	loginSMTP(password)
	loginIMAP(password)
	# Now we have an IMAP object too.

def getPositionOfWord(move):
	'''
	This finds the middle of the word, and then uses simple comparisons to find what quadrant it is, returning a descriptor of that quadrant.
	'''
	print "Move:", move
	r, c = move[1],move[2]
	if move[3] == "down":
		c = (c + c - len(move[0]))/2
	else:
		r = (r + r - len(move[0]))/2
	if r > 7:
		if c > 7:
			return "bottom-right quadrant"
		else:
			return "bottom-left quadrant"
	else:
		if c > 7:
			return "top-right quadrant"
		else:
			return "top-left quadrant"

def getAttachedWord(grid,move,specifyAttachedLetter=False):
	'''
	This finds the first word that is attached to the word you are placing, and returns a message saying this.
	'''
	r,c = move[1],move[2]
	for i in range(len(move[0])):
		# For each letter in the word:
		if move[3] == "across":
			backword = ""
			for j in range(r-1,-1,-1):
				if grid[j][c-i] != " ":
					backword = grid[j][c-i] + backword
				else: break
			forword = ""
			for j in range(r+1,15):
				if grid[j][c-i] != " ":
					forword += grid[j][c-i]
				else: break
			attachedWord = backword + grid[r][c-i] + forword
			if len(attachedWord) > 1:
				if specifyAttachedLetter:
					return "across from the "+grid[r][c-i]+" in "+attachedWord
				else:
					return attachedWord
		else:
			backword = ""
			for j in range(c-1,-1,-1):
				if grid[r-i][j] != " ":
					backword = grid[r-i][j] + backword
				else: break
			forword = ""
			for j in range(c+1,15):
				if grid[r-i][j] != " ":
					forword += grid[r-i][j]
				else: break
			attachedWord = backword + grid[r-i][c] + forword
			if len(attachedWord) > 1:
				if specifyAttachedLetter:
					return "down from the "+grid[r-i][c]+" in "+attachedWord
				else:
					return attachedWord

def getLettersOfWord(move):
	'''
	This returns the letters present in a word, alphabetised.
	'''
	letters = []
	for i in move[0]:
		letters.append(i)
	letters.sort()
	return ", ".join(letters)

def prettyReturnGrid(grid,moveToDisplay):
	'''
	This returns a formatted representation of part of the grid.
	'''
	# Build a box around the centre of a word.
	r, c = moveToDisplay[1],moveToDisplay[2]
	if moveToDisplay[3] == "down":
		c = (c + c - len(moveToDisplay[0]))/2
	else:
		r = (r + r - len(moveToDisplay[0]))/2
	size = len(moveToDisplay[0]) + 1
	first = (r-size,c-size)
	second = (r+size,c+size)
	gridString = ""
	for i in range(first[0],second[0]+1):
		if i in range(15):
			s = "..."
			for j in range(first[1],second[1]+1):
				if j in range(15):
					s += grid[i][j] + ","
			gridString += s[:-1] + "...\n"
	return gridString

def generateEmail(bestgrid, simplegrid, bestmove, simplemove):
	'''
	Produces the main string of the email!
	'''
	mailString = "Subject: Words With Friends (requested " + time.ctime() + ")\n"
	mailString += "Hello!\n\nYou asked for help with a certain Words With Friends puzzle. Good news, we found a solution! But first, some hints, just in case you want to improve first."
	mailString += "\n\nHint #1: The best move is located in the "+getPositionOfWord(bestmove)+", attached to (or creating) the word "+getAttachedWord(bestgrid,bestmove)+"."
	mailString += "\nIf you're only looking at commonly used words, the best move is in the "+getPositionOfWord(simplemove)+", attached to (or creating) the word "+getAttachedWord(simplegrid,simplemove)+"."
	# TODO: actually write email.
	mailString += "\n"*8
	mailString += "Hint #2: The best move uses the letters "+getLettersOfWord(bestmove)+"."
	mailString += "\nIf you're only looking at commonly used words, the best move uses the letters "+getLettersOfWord(simplemove)+"."
	mailString += "\n"*8
	mailString += "Solution: "+bestmove[0]+", which is "+getAttachedWord(bestgrid,bestmove,True)+". The last letter is at position ("+str(bestmove[2]+1)+","+str(bestmove[1]+1)+"). This may be more easily read from this image:\n"
	mailString += prettyReturnGrid(bestgrid,bestmove)
	mailString += "\nIf you are only looking at commonly used words, you'll instead be looking at "+simplemove[0]+", which is "+getAttachedWord(simplegrid,simplemove,True)+". The last letter is at position ("+str(simplemove[1]+1)+","+str(simplemove[2]+1)+"). This may be more easily read from this image:\n"
	mailString += prettyReturnGrid(simplegrid,simplemove)
	mailString += "\nThank you for using the service today!"
	return mailString

def sendMail(bestgrid,simplegrid,recipient,bestmove,simplemove):
	'''
	This creates an email, and then sends it off!
	'''
	print "Creating email!"
	if smtpObj:
		mailString = generateEmail(bestgrid,simplegrid,bestmove,simplemove)
		success = smtpObj.sendmail(myEmail,recipient,mailString)
		count = 0
		emailSent = False
		while not emailSent:
			print smtpObj.docmd("NOOP")
			if smtpObj.docmd("NOOP")[0] == 250:
				while success != {} and count < 5:
					success = smtpObj.sendmail(myEmail,recipient,mailString)
					count += 1
				if count >= 5:
					print "ERROR ERROR ERROR"
				else:
					print "Email sent!"
					emailSent = True
			else:
				logoutSMTP()
				loginSMTP(pswd)
	else:
		print "Not connected."

def sendFailureMail(error, recipient):
	'''
	Sends a message with an error, because something went wrong...
	'''
	if smtpObj:
		mailString = "Subject: Words With Friends (requested " + time.ctime() + ")\nWe're sorry, but the program returned an error. Maybe take another screenshot and resend it?\nError: "+error
		success = smtpObj.sendmail(myEmail,recipient,mailString)
		count = 0
		if smtpObj.docmd("NOOP")[0] == 250:
			while success != {} and count < 5:
				success = smtpObj.sendmail(myEmail,recipient,mailString)
				count += 1
			if count >= 5:
				print "ERROR ERROR ERROR"
			else:
				print "Email sent!"
		else:
			logoutSMTP()
			loginSMTP(pswd)
			sendFailureMail(error, recipient)
	else:
		print "Not connected."

def logoutSMTP():
	if smtpObj:
		smtpObj.quit()

def logoutIMAP():
	if idler:
		idler.stop()
		idler.join()
	if imapObj:
		imapObj.close()
		imapObj.logout()

def restartIMAP():
	logoutIMAP()
	loginIMAP(pswd)
	t = Timer(1200.0,restartIMAP)
	t.start()

def logout():
	logoutSMTP()
	logoutIMAP()

'''
This class is taken (and modified) from:
http://blog.hokkertjes.nl/posts/2009/03/11/python-imap-idle-with-imaplib2.html
'''
class Idler(object):
	def __init__(self, conn):
		self.thread = Thread(target=self.idle)
		self.M = conn
		self.event = Event()

	def start(self):
		self.thread.start()

	def stop(self):
		# This is a neat trick to make thread end. Took me a 
		# while to figure that one out!
		self.event.set()

	def join(self):
		self.thread.join()

	def idle(self):
		# Starting an unending loop here
		while True:
			# This is part of the trick to make the loop stop 
			# when the stop() command is given
			if self.event.isSet():
				return
			self.needsync = False
			# A callback method that gets called when a new 
			# email arrives. Very basic, but that's good.
			def callback(args):
				if not self.event.isSet():
					self.needsync = True
					self.event.set()
			# Do the actual idle call. This returns immediately, 
			# since it's asynchronous.
			self.M.idle(callback=callback)
			# This waits until the event is set. The event is 
			# set by the callback, when the server 'answers' 
			# the idle call and the callback function gets 
			# called.
			self.event.wait()
			# Because the function sets the needsync variable,
			# this helps escape the loop without doing 
			# anything if the stop() is called. Kinda neat 
			# solution.
			if self.needsync:
				self.event.clear()
				self.dosync()

	# The method that gets called when a new email arrives. 
	def dosync(self):
		print "Got an email!"
		result, data = imapObj.uid("search", None, "UNSEEN")
		print data
		if result == "OK":
			loginSMTP(pswd)
			for mailuid in data[0].split():
				emailResult, emailData = imapObj.uid("fetch",mailuid,"(RFC822)")
				if emailResult == "OK":
					emailmessage = email.message_from_string(emailData[0][1])
					print email.utils.parseaddr(emailmessage["From"])
					for part in emailmessage.get_payload():
						print part.get_content_type()
						if part.get_content_type() == 'image/png':
							open("screenshot.png","wb").write(part.get_payload(decode=True))
							solveGrid("screenshot.png",emailmessage["Subject"],emailmessage["From"])
						elif part.get_content_type() == 'image/jpeg':
							open("screenshot.jpeg","wb").write(part.get_payload(decode=True))
							solveGrid("screenshot.jpeg",emailmessage["Subject"],emailmessage["From"])
					imapObj.store(mailuid, "+FLAGS", "\\Deleted")
			logoutSMTP()
		imapObj.expunge()

def solveGrid(filename,tiles,recipient):
	'''
	Takes the important content of the email, passes it around and then sends an email with the results.
	'''
	print "Let's solve!"
	# Solve the things (pass to imageprocessing, pass grid to solver and then return here), then
	chosenTiles = []
	for i in tiles:
		if i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ_":
			chosenTiles.append(i)
		if i=="?":
			chosenTiles.append("_")
	bestgrid, simplegrid, bestmove, simplemove, emptyGrid = processImage(filename,chosenTiles)
	if emptyGrid:
		sendFailureMail("Couldn't read the grid.",recipient)
	elif bestmove == False and simplemove == False:
		sendFailureMail("No solutions were found",recipient)
	else:
		#print generateEmail(bestgrid,simplegrid,bestmove,simplemove)
		sendMail(bestgrid,simplegrid,recipient,bestmove,simplemove)
	os.remove(filename)

def emailSetup(password):
	'''
	Sets up the email system.
	'''
	atexit.register(logout)
	global pswd
	pswd = password
	print "Setting up email!"
	login(password)
	t = Timer(1200.0,restartIMAP)
	t.start()
	imageProcessingSetup()
	while True:
		pass

if __name__ == '__main__':
	emailSetup(raw_input("Enter password: "))