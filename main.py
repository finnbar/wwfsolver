from emailSender import *
import getpass

if __name__ == '__main__':
	emailSetup(getpass.getpass("Enter password: ")) # This in turn sets up imageProcessing and solver.