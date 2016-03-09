import re

ignore = ['__builtins__','__name__','__doc__','__package__']
a = re.compile("\'.+\'")

def printLocals(name,locs):
	print "Variables in "+name
	for i in locs:
		if not i in ignore:
			print str(i) + "(" + a.search(str(type(i))).group()[1:-1] + ")"