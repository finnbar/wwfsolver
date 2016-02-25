from PIL import Image
import os, copy
from solver import *
borderEdgeX = 4 # Border between edge and start of grid
borderEdgeY = 306
borderX = 4 # Border between two edges of squares (left to right)
borderY = 4 # Border between two edges of squares (up to down)
sizeX = 68 # Box size
sizeY = 68 # Box size
comparisonData = {}

def getCoords(x,y):
	'''
	Takes a coordinate (x,y) for the grid and turns it into four pixel values on the screenshot.
	(left, up, right, down)
	'''
	l = borderEdgeX + ((sizeX + borderX) * x)
	u = borderEdgeY + ((sizeY + borderY) * y)
	return (l,u,l+sizeX,u+sizeY)

def parseGrid(image):
	'''
	Take the screenshot (image), split it into each individual square on the grid and then colour them simply (essentially making the contrast super high), making an indexable ImageGrid.
	'''
	ImageGrid = [["" for i in range(15)] for j in range(15)]
	for i in range(15):
		for j in range(15):
			ImageGrid[i][j] = image.crop(getCoords(i,j))
			ImageGrid[i][j] = ImageGrid[i][j].convert("L")
			ImageGrid[i][j] = ImageGrid[i][j].point(lambda x: (255,0)[x > 225 or x < 100])
	return ImageGrid

def compareImages(i1,i2):
	'''
	Takes two images (i1,i2) and works out the number of pixels that are different between the images (error).
	'''
	# Returns the error between two images.
	d1 = list(i1.getdata())
	d2 = list(i2.getdata())
	# Now loop through, count number of same squares and then store that.
	error = 0
	assert len(d1) == len(d2)
	for i in range(len(d1)):
		if d1[i] != d2[i]: error += 1
	return error

def identifySquare(square):
	'''
	Compares the given square (square) to each of the tiles in comparisonData in order to work out what letter the square contains.
	'''
	lowestError = 250 # How much error is allowed before deeming an image as not being a letter.
	bestFit = ""
	for i in comparisonData:
		err = compareImages(square,comparisonData[i])
		if err < lowestError:
			lowestError = err
			bestFit = i
	return bestFit

def readGrid(imageGrid, verbose=False):
	'''
	Take an ImageGrid (imageGrid) and identify each square in turn (with identifySquare), assembling a Grid (that solver.py can understand) in the process. Note that because solver.py's Grids use Grid[row][column] and ImageGrid uses ImageGrid[x][y], the coordinates are swapped.
	'''
	grid = [[" " for j in range(15)] for i in range(15)]
	for i in range(15):
		for j in range(15):
			if imageGrid[i][j] != "":
				grid[j][i] = identifySquare(imageGrid[i][j])
				if grid[j][i] == "":
					grid[j][i] = " "
					if verbose: print "Tile at",j,i,"not recognised"
	return grid

def loadComparisonData(folder):
	'''
	Take a folder name (folder), and load all of the images in it as comparisonData. This data is used to work out how close a square is to an example letter.
	'''
	for i in os.listdir(folder):
		comparisonData.update({i[0]: Image.open(folder+"/"+i)})
	return len(os.listdir(folder))

def createComparisonData(folder):
	'''
	Take a folder name (folder), and use the images in there to create the comparisonData.
	'''
	screenshot = Image.open("exampleScreenshots/DLJzVwV.png")
	ImageGrid = parseGrid(screenshot)
	ImageGrid[0][0].show()
	saveData = {"A": ImageGrid[9][3], "B": ImageGrid[7][6], "C": ImageGrid[7][3], "D": ImageGrid[9][5], "E": ImageGrid[2][2], "F": ImageGrid[0][8], "G": ImageGrid[11][2], "H": ImageGrid[14][13], "I": ImageGrid[3][4], "J": ImageGrid[9][9], "L": ImageGrid[0][6], "M": ImageGrid[13][7], "N": ImageGrid[0][3], "O": ImageGrid[9][7], "P": ImageGrid[13][5], "Q": ImageGrid[3][0], "R": ImageGrid[7][5], "S": ImageGrid[11][5], "T": ImageGrid[2][3], "U": ImageGrid[7][4], "V": ImageGrid[14][3], "W": ImageGrid[8][7], "X": ImageGrid[10][3], "Y": ImageGrid[2][1],"Z": ImageGrid[13][10]} 
	for i in saveData:
		saveData[i].save(folder+"/"+i+".png")
	# Because that screenshot didn't contain K, we need to look at another one.
	screenshot = Image.open("exampleScreenshots/NMUJj39.png")
	ImageGrid = parseGrid(screenshot)
	ImageGrid[5][13].save(folder+"/K.png")
	# Silly K.

def processImage(filename,chosenTiles):
	'''
	Takes a screenshot, and turns it into a grid, executing each of the functions required in turn. Then ask the solver for the solution with findBothSolutions.
	'''
	screenshot = Image.open(filename)
	screenshot.show()
	ImageGrid = parseGrid(screenshot)
	Grid = readGrid(ImageGrid)
	Grid2 = copy.deepcopy(Grid)
	empty = True # Assume empty until something's found.
	for i in Grid:
		for j in i:
			if j != " ":
				empty = False
				break
		if not empty:
			break
	if not empty:
		bestgrid, simplegrid = False, False
		fullSol, simpleSol = findBothSolutions(Grid,chosenTiles,True)
		if not (fullSol == False):
			bestgrid = placeOnGrid(Grid,findPlacements(Grid,fullSol),fullSol[0])
		if not (simpleSol == False):
			simplegrid = placeOnGrid(Grid2,findPlacements(Grid2,simpleSol),simpleSol[0])
		return bestgrid, simplegrid, fullSol, simpleSol, False
	return False, False, False, False, True

def imageProcessingSetup():
	'''
	Make sure that the comparisonData exists and is loaded, and set up the solver (the included module).
	'''
	if loadComparisonData("data") == 0:
		createComparisonData("data")
		loadComparisonData("data")
	solverSetup() # Also sets up the stage above

if __name__ == '__main__':
	imageProcessingSetup()
	bestgrid,simplegrid,fullSol,simpleSol,error = processImage("exampleScreenshots/yqnnbJI.png",["A","_","E","B","C","D","J"])
	if(error): print "ERROR"
	prettyPrint(bestgrid)
	print ""
	prettyPrint(simplegrid)
	print fullSol, simpleSol