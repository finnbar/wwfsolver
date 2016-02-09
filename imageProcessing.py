from PIL import Image
borderEdgeX = 1 # Border between edge and start of grid
borderEdgeY = 323
borderX = 2 # Border between two edges of squares (left to right)
borderY = 3 # Border between two edges of squares (up to down)
sizeX = 46 # Box size
sizeY = 45 # Box size
tileColours = [(177,85,75),(177,85,76),(17,127,187),(15,126,186),(16,126,186),(107,160,85),(234,152,46),(193,200,207),(234,151,46)] # These are the colours of empty tiles, so ignore these

def openImage(location):
    return Image.open(location)

def getCoords(x,y):
    # Turns an x,y coord for the grid into four pixel values
    # (left, up, right, down)
    l = borderEdgeX + ((sizeX + borderX) * x)
    u = borderEdgeY + ((sizeY + borderY) * y)
    return (l,u,l+sizeX,u+sizeY)

def parseGrid(image,palette):
    ImageGrid = [["" for i in range(15)] for j in range(15)]
    for i in range(15):
        for j in range(15):
            ImageGrid[i][j] = image.crop(getCoords(i,j))
            testPixel = ImageGrid[i][j].getpixel((6,6))
            if not testPixel in tileColours:
                ImageGrid[i][j] = ImageGrid[i][j].convert("L")
                ImageGrid[i][j].putpalette(palette)
                ImageGrid[i][j] = ImageGrid[i][j].convert("L")
            else:
                # Delete, this is an empty tile.
                ImageGrid[i][j] = ""
    return ImageGrid

def setupPalette():
    letterFindPalette = [255 for i in range(768)]
    for i in range(4):
        letterFindPalette[i] = 0
        letterFindPalette[-i] = 0
    return letterFindPalette

def compareImages(i1,i2):
    # Returns the error between two images.
    d1 = list(i1.getdata())
    d2 = list(i2.getdata())
    # Now loop through, count number of same squares and then store that.
    error = 0
    assert len(d1) == len(d2)
    for i in range(len(d1)):
        if d1[i] != s1[i]: error += 1
    return error

# TODO: Collect test data from screenshot.
# Win.

if __name__ == '__main__':
    screenshot = openImage("Screenshot.png")
    letterFindPalette = setupPalette()
    ImageGrid = parseGrid(screenshot, letterFindPalette)
    ImageGrid[4][7].show()
