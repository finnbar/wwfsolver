from PIL import Image
import os
borderEdgeX = 3 # Border between edge and start of grid
borderEdgeY = 110
borderX = 5 # Border between two edges of squares (left to right)
borderY = 6 # Border between two edges of squares (up to down)
sizeX = 19 # Box size
sizeY = 18 # Box size
# bEX, bEY, bX, bY, sX, sY = 1, 323, 2, 3, 46, 45 for exampleScreenshot768
tileColours = [(177,85,75),(177,85,76),(17,127,187),(15,126,186),(16,126,186),(107,160,85),(234,152,46),(193,200,207),(234,151,46)] # These are the colours of empty tiles, so ignore these
comparisonData = {}

def openImage(location):
	return Image.open(location)

def getCoords(x,y):
	# Turns an x,y coord for the grid into four pixel values
	# (left, up, right, down)
	l = borderEdgeX + ((sizeX + borderX) * x)
	u = borderEdgeY + ((sizeY + borderY) * y)
	return (l,u,l+sizeX,u+sizeY)

def parseGrid(image):
	ImageGrid = [["" for i in range(15)] for j in range(15)]
	for i in range(15):
		for j in range(15):
			ImageGrid[i][j] = image.crop(getCoords(i,j))
			testPixel = ImageGrid[i][j].getpixel((6,6))
			if not testPixel in tileColours:
				ImageGrid[i][j] = ImageGrid[i][j].convert("L")
				ImageGrid[i][j] = ImageGrid[i][j].point(lambda x: (255,0)[x > 225 or x < 100])
			else:
				# Delete, this is an empty tile.
				ImageGrid[i][j] = ""
	return ImageGrid

def identifySquare(tile):
	lowestError = 20
	bestFit = ""
	for i in comparisonData:
		err = compareImages(tile,comparisonData[i])
		if err < lowestError:
			lowestError = err
			bestFit = i
	return bestFit

def compareImages(i1,i2):
	# Returns the error between two images.
	d1 = list(i1.getdata())
	d2 = list(i2.getdata())
	# Now loop through, count number of same squares and then store that.
	error = 0
	assert len(d1) == len(d2)
	for i in range(len(d1)):
		if d1[i] != d2[i]: error += 1
	return error

# TODO: Collect test data from screenshot.
# Win.

def loadComparisonData(folder):
	for i in os.listdir(folder):
		comparisonData.update({i[0]: Image.open(folder+"/"+i)})
	return len(os.listdir(folder))

def createComparisonData(folder):
	# This function creates an image for each letter, which will be useful as we can compare unknown tiles to these known ones and look for similarities!
	screenshot = openImage("exampleScreenshot362.png")
	ImageGrid = parseGrid(screenshot)
	saveData = {"C": ImageGrid[6][7], "U": ImageGrid[7][7], "L": ImageGrid[8][7], "T": ImageGrid[9][7], "I": ImageGrid[9][8], "G": ImageGrid[9][9], "A": ImageGrid[8][9], "F": ImageGrid[7][9], "V": ImageGrid[7][11], "E": ImageGrid[7][12]}
	for i in saveData:
		saveData[i].save(folder+"/"+i+".png")

if __name__ == '__main__':
	screenshot = openImage("exampleScreenshot362.png")
	screenshot.show()
	ImageGrid = parseGrid(screenshot)
	ImageGrid[7][7].show()
	ImageGrid[7][10].show()
	ImageGrid[7][11].show()
	ImageGrid[9][7].show()
	print "Comparing As:",compareImages(ImageGrid[7][10],ImageGrid[8][9])
	print "Comparing T and I:",compareImages(ImageGrid[9][7],ImageGrid[9][8])
	if loadComparisonData("data-362") == 0:
		createComparisonData("data-362")
		loadComparisonData("data-362")
	print identifySquare(ImageGrid[7][10])