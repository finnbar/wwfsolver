from emailSender import *
import getpass

if __name__ == '__main__':
	print "Running!"
	emailSetup(getpass.getpass("Enter password: ")) # This in turn sets up imageProcessing and solver.