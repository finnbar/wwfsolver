import imaplib2,smtplib,time,email
from threading import *
from solver import *
from imageProcessing import *
myEmail = "wordswithfriendssolver@gmail.com"

def login():
	global idler
	smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
	assert smtpObj.ehlo()[0] == 250
	smtpObj.starttls()
	smtpObj.login(myEmail,"thissolverisamazing")
	print "SMTP done!"
	# TODO: SECURELY STORE PASSWORD, FINNBAR.
	# Anyway, we now have an SMTP object, which can be passed to other functions
	imapObj = imaplib2.IMAP4_SSL("imap.googlemail.com")
	imapObj.login(myEmail,"thissolverisamazing")
	imapObj.select("INBOX")
	idler = Idler(imapObj)
	idler.start()
	print "IMAP done!"
	# Now we have an IMAP object too.
	return imapObj,smtpObj

def receiveMail():
	imapObj.select("inbox")
	result, data = imapObj.uid("search", None, "UNSEEN")
	# TODO: Write rest of function here, using email library to parse the email afterwards
	# See:
	# https://yuji.wordpress.com/2011/06/22/python-imaplib-imap-example-with-gmail/
	# https://docs.python.org/2/library/imaplib.html

def sendMail(recipient,bestmove,simplemove):
	if smtpObj:
		mailString = "Subject: Words With Friends (requested " + time.ctime() + ")\n"
		mailString += "Hello!\n\nYou asked for help with a certain Words With Friends puzzle. Good news, we found a solution! But first, some hints, just in case you want to improve first."
		mailString += "\n\nHint #1: The best move is located in the "
		# TODO: actually write email.
		success = smtpObj.sendmail(myEmail,recipent,mailString)
		count = 0
		while success != {} and count < 5:
			success = smtpObj.sendmail(myEmail,recipent,mailString)
			count += 1
		if count >= 5:
			print "ERROR ERROR ERROR"
		else:
			print "Email sent!"
	else:
		print "Not connected."

def logout():
	if smtpObj:
		smtpObj.quit()
	if idler:
		idler.stop()
		idler.join()
	if imapObj:
		imapObj.logout()

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
		if result == "OK":
			for mailuid in data[0].split():
				emailResult, emailData = imapObj.uid("fetch",mailuid,"(RFC822)")
				if emailResult == "OK":
					emailmessage = email.message_from_string(emailData[0][1])
					print email.utils.parseaddr(emailmessage["From"])
					for part in emailmessage.get_payload():
						print part.get_content_type()
						if part.get_content_type() == 'image/png':
							open("screenshot.png","wb").write(part.get_payload(decode=True))
							solveGrid("screenshot.png",emailmessage["From"])
						elif part.get_content_type() == 'image/jpeg':
							open("screenshot.jpeg","wb").write(part.get_payload(decode=True))
							solveGrid("screenshot.jpeg",emailmessage["From"])
					imapObj.store(mailuid, "+FLAGS", "\\Deleted")
		imapObj.expunge()

def solveGrid(filename,recipient):
	print "Let's solve!"
	# Solve the things (pass to imageprocessing, pass grid to solver and then return here), then
	#os.remove(filename)

def emailSetup():
	global imapObj,smtpObj
	imapObj,smtpObj = login()
	raw_input("Press enter to finish.")
	logout()

if __name__ == '__main__':
	emailSetup()