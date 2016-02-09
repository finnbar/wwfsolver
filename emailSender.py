import imapclient
import smtplib
import time
smtpObj = False
imapObj = False
myEmail = "wordswithfriendssolver@gmail.com"

def login():
    smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
    assert smtpObj.ehlo()[0] == 250
    smtpObj.starttls()
    smtpObj.login(myEmail,"thissolverisamazing")
    print "SMTP done!"
    # TODO: SECURELY STORE PASSWORD, FINNBAR.
    # Anyway, we now have an SMTP object, which can be passed to other functions
    imapObj = imapclient.IMAPClient("imap.googlemail.com")
    imapObj.login(myEmail,"thissolverisamazing")
    print "IMAP done!"
    # Now we have an IMAP object too.
    return imapObj,smtpObj

def receiveMail():
    if imapObj:
        imapObj.select_folder("INBOX", readonly=False)
        UIDs = imapObj.search(["UNSEEN"])
        rawMessages = imapObj.fetch(UIDs,['BODY[]', 'FLAGS'])
        
        for i in rawMessages:
            message = pyzmail.PyzMessage.factory(i['BODY[]'])
            message.get_addresses("from")
    
def sendMail(recipient,bestmove,simplemove=()):
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
    if imapObj:
        imapObj.quit()
    # Then make the objects false again.

if __name__ == '__main__':
    global imapObj,smtpObj
    imapObj,smtpObj = login()
