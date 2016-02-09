import pickle

Grid = [[" " for j in range(15)] for i in range(15)]
Modifiers = [[" " for j in range(15)] for i in range(15)]
Scores = {"_": 0, "A": 1, "E": 1, "I": 1, "O": 1, "T": 1, "R": 1, "S": 1, "L": 2, "U": 2, "D": 2, "N": 2, "Y": 3, "G": 3, "H": 3, "B": 4, "C": 4, "F": 4, "M": 4, "P": 4, "W": 4, "K": 5, "V": 5, "X": 8, "J": 10, "Q": 10, "Z": 10}
WordList = []
Dictionary = {}

def prettyPrint(g):
    for i in range(15):
        s = ""
        for j in range(15):
            s += g[i][j] + ","
        print s[:-1]

def placeOnGrid(g,p,word):
    # p is placements
    for i in range(len(p)):
        g[p[i][0]][p[i][1]] = word[i]
    # (may need to write helper "findPlacements" function)
    return g

def findPlacements(g,solution):
    placements = []
    w,sx,sy = solution[0],solution[1],solution[2]
    if solution[3] == "down":
        for i in range(sx-len(w)+1,sx+1):
            g[i][sy] = w[i+len(w)-1-sx]
    else:
        for i in range(sy-len(w)+1,sy+1):
            g[sx][i] = w[i+len(w)-1-sy]
    return placements

def findAllWords(g,line,tiles,row,column,word,flipped,attached=False):
    possibles = line[column][1:] # Ignore the bonus string...
    for possible in possibles:
        if possible in tiles or line[column][0] == "board":
            if isPartOfWord(word+possible):
                # Check if there's a tile next to it, if so, mark as so.
                # This means checking if we've got one above or below.
                if row - 1 > 0:
                    if g[row-1][column] != " ":
                        attached = True
                if row + 1 < 15:
                    if g[row+1][column] != " ":
                        attached = True
                if isCompletedWord(word+possible) and attached:
                    # Last check: is this the end of a word?:
                    orientation = ["across","down"][flipped]
                    c = [column,row][flipped]
                    r = [row,column][flipped]
                    if column + 1 < 15:
                        if g[row][column+1] == " ":
                            if not (word+possible,r,c,orientation) in WordList:
                                WordList.append((word+possible,r,c,orientation))
                    else:
                        if not (word+possible,r,c,orientation) in WordList:
                            WordList.append((word+possible,r,c,orientation))
                if line[column][0] == "tiles":
                    newTiles = tiles[:]
                    newTiles.remove(possible)
                    if column + 1 < 15:
                        findAllWords(g,line,newTiles,row,column+1,word+possible,flipped,attached)
                else:
                    # So we didn't add anything, but we have to continue.
                    # This allows you to continue words.
                    if column + 1 < 15:
                        findAllWords(g,line,tiles,row,column+1,word+possible,flipped,True)

def doRows(grid,tiles,flipped=False):
    # Work up to down on the current grid:
    for i in range(15):
        line = grid[i][:]
        for j in range(15):
            if line[j] != " ":
                # if it's already a letter, we're done.
                line[j] = ["board",line[j]]
            else:
                line[j] = ["tiles"]
                backword = ""
                for k in range(i-1,-1,-1):
                    if grid[k][j] == " ": break
                    backword = grid[k][j] + backword
                forword = ""
                for k in range(i+1,15):
                    if grid[k][j] == " ": break
                    forword += grid[k][j]
                for t in tiles:
                    if len(backword + t + forword) == 1 or isCompletedWord(backword + t + forword):
                        line[j].append(t)
        for q in range(15):
            if q > 0:
                if line[q-1][0] == "tiles":
                    findAllWords(grid,line,tiles,i,q,"",flipped)
            else:
                findAllWords(grid,line,tiles,i,q,"",flipped)

def doColumns(grid,tiles):
    # Flip the rows and columns
    grid = [[grid[i][j] for i in range(15)] for j in range(15)]
    doRows(grid,tiles,True)

def scoreMove(word,grid,modifiers,verbose=False):
    # word = ("word",x,y,"across or down")
    if word[3] == "down":
        # Flip the grid, and run with that!
        g = [[grid[i][j] for i in range(15)] for j in range(15)]
        m = [[modifiers[i][j] for i in range(15)] for j in range(15)]
        w = (word[0],word[2],word[1],"across")
        return scoreMove(w,g,m,verbose)
    score = 0
    extraScore = 0
    wordModifiers = [] # Modifiers that affect the whole word (TW,DW)
    placements = []
    if verbose: prettyPrint(grid)
    for i in range(len(word[0])):
        onGrid = False
        if grid[word[1]][word[2]-i] != " ": onGrid = True
        placements.append((word[0][len(word[0])-1-i],word[1],word[2]-i,onGrid))
    # Score the main word:
    if verbose: print(placements)
    for tile in placements:
        wordModifiers,tileScore = scoreLetter(tile,grid,modifiers,wordModifiers,verbose)
        score += tileScore
        # Now, check if any new words are created, but only...
        if not tile[3]: # ...if it was placed this turn.
            anotherWord = False
            bonusScore = 0
            bonusWordModifiers = []
            if grid[tile[1]+1][tile[2]] != " ":
                anotherWord = True
                for k in range(tile[1]+1,15):
                    if grid[k][tile[2]] == " ": break
                    bonusWordModifiers,s = scoreLetter((grid[k][tile[2]],k,tile[2]),grid,modifiers,bonusWordModifiers,verbose)
                    bonusScore += s
            if grid[tile[1]-1][tile[2]] != " ":
                anotherWord = True
                for k in range(tile[1]-1,-1,-1):
                    if grid[k][tile[2]] == " ": break
                    bonusWordModifiers,s = scoreLetter((grid[k][tile[2]],k,tile[2]),grid,modifiers,bonusWordModifiers,verbose)
                    bonusScore += s
            if anotherWord:
                bonusWordModifiers,s = scoreLetter(tile,grid,modifiers,bonusWordModifiers,verbose)
                bonusScore += s # It's used in another word, add its score again
                bonusScore = wordMultiplier(bonusScore,bonusWordModifiers)
                if verbose: print("We've added another word! Bonus is ",bonusScore)
                extraScore += bonusScore
    score = wordMultiplier(score,wordModifiers)
    return score + extraScore

def wordMultiplier(score,wordModifiers):
    for modifier in set(wordModifiers):
        if modifier == "DW":
            score *= 2
        elif modifier == "TW":
            score *= 3
    return score

def scoreLetter(tile,grid,modifiers,wordModifiers,verbose):
    if grid[tile[1]][tile[2]] == " ":
        modifier = modifiers[tile[1]][tile[2]]
        if modifier == "DL": # Double Letter
            score = 2*Scores[tile[0]]
        elif modifier == "TL": # Triple Letter
            score = 3*Scores[tile[0]]
        else:
            score = Scores[tile[0]]
            if modifier != " ":
                wordModifiers.append(modifier)
    else:
        score = Scores[tile[0]]
    if verbose: print(tile[0],"is worth",score,"!")
    return wordModifiers,score

def isPartOfWord(word):
    partOfDictionary = Dictionary
    for letter in word:
        if letter in partOfDictionary:
            partOfDictionary = partOfDictionary[letter]
        else:
            return False
    return True

def isCompletedWord(word):
    partOfDictionary = Dictionary
    for letter in word:
        if letter in partOfDictionary:
            partOfDictionary = partOfDictionary[letter]
        else:
            return False
    return partOfDictionary["acc"]

def parseDictionary(d):
    Dictionary = {}
    for word in d:
        word = word.replace("\n","")
        previousIndex = Dictionary
        counter = len(word)
        for letter in word.upper():
            counter -= 1
            if not (letter in previousIndex):
                previousIndex[letter] = {"acc": False}
            previousIndex = previousIndex[letter]
            if counter == 0:
                previousIndex["acc"] = True
    return Dictionary

def importDictionary(filename):
    global Dictionary
    f = file(filename,"r")
    words = []
    data = f.readline()
    while data:
        words.append(data)
        data = f.readline()
    Dictionary = parseDictionary(words)
    d = file("dictionary.txt","w")
    pickle.dump(Dictionary,d)
    d.close()

def loadDictionary(filename):
    global Dictionary
    f = file(filename,"r")
    Dictionary = pickle.load(f)

def outputToFile(filename,variable):
    f = file(filename,"w")
    f.write(str(variable))
    f.close

def testRoutine():
    Grid[7][6] = "A"
    Grid[7][7] = "P"
    Grid[7][8] = "P"
    Grid[7][9] = "L"
    Grid[7][10] = "E"
    Grid[7][11] = "S"
    Grid[6][8] = "E"
    Grid[8][8] = "S"
    Grid[9][8] = "I"
    Grid[10][8] = "L"
    Grid[11][8] = "O"
    Grid[12][8] = "N"
    Grid[10][5] = "H"
    Grid[10][6] = "E"
    Grid[10][7] = "L"
    Grid[10][9] = "O"
    Grid[6][10] = "B"
    Grid[8][10] = "T"
    Grid[9][10] = "A"
    chosenTiles = ["A","B","A","Z","Q","V"]
    prettyPrint(Grid)
    doRows(Grid,chosenTiles)
    doColumns(Grid,chosenTiles)
    HighestScore = 0
    WordNumber = 0
    for i in range(len(WordList)):
        s = scoreMove(WordList[i],Grid,Modifiers)
        if s > HighestScore:
            HighestScore = s
            WordNumber = i
    newGrid = placeOnGrid(Grid, findPlacements(Grid,WordList[WordNumber]), WordList[WordNumber][0])
    print
    prettyPrint(newGrid)
    print(WordList[WordNumber],HighestScore)

if __name__ == '__main__':
    solverSetup()

def solverSetup():
    loadDictionary("dictionary.txt")
    # Add to Modifiers. The Grid has two lines of reflection, so we define the top quarter and then reflect:
    Modifiers[0][3] = "TW"
    Modifiers[0][6] = "TL"
    Modifiers[1][2] = "DL"
    Modifiers[1][5] = "DW"
    Modifiers[2][1] = "DL"
    Modifiers[2][4] = "DL"
    Modifiers[3][0] = "TW"
    Modifiers[3][3] = "TL"
    Modifiers[3][7] = "DW"
    Modifiers[4][2] = "DL"
    Modifiers[4][6] = "DL"
    Modifiers[5][1] = "DW"
    Modifiers[5][5] = "TL"
    Modifiers[6][0] = "TL"
    Modifiers[6][4] = "DL"
    Modifiers[7][3] = "DW"
    Modifiers[7][7] = "DW"
    # And reflect
    for x in range(8):
        for y in range(8):
            Modifiers[14-x][14-y] = Modifiers[x][y]
            Modifiers[14-x][y] = Modifiers[x][y]
            Modifiers[x][14-y] = Modifiers[x][y]