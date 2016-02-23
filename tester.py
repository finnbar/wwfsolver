from solver import *

if __name__ == '__main__':
    solverSetup()
    Grid = [[" " for j in range(15)] for i in range(15)]
    chosenTiles = []
    testNumber = int(raw_input("What test do you want to run? "))
    if testNumber == 1:
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
        chosenTiles = ["A","B","A","Z","Q","V","_"]
    elif testNumber == 2:
        Grid[0][0] = "A"
        Grid[0][1] = "C"
        Grid[0][2] = "T"
        Grid[0][4] = "R"
        Grid[0][5] = "S"
        Grid[1][1] = "A"
        Grid[2][1] = "T"
        Grid[3][1] = "T"
        Grid[4][1] = "L"
        Grid[5][1] = "E"
        Grid[1][4] = "A"
        Grid[2][4] = "N"
        Grid[3][4] = "G"
        Grid[4][4] = "E"
        chosenTiles = ["O","R","S"]
    elif testNumber == 3:
        Grid[6][6] = "D"
        Grid[7][6] = "E"
        Grid[8][6] = "L"
        Grid[9][6] = "I"
        chosenTiles = ["Q","U","E","E","N"]
    elif testNumber == 4:
        Grid[5][6] = "B"
        Grid[5][7] = "O"
        Grid[5][8] = "R"
        Grid[5][9] = "E"
        Grid[6][7] = "I"
        Grid[7][3] = "S"
        Grid[7][4] = "A"
        Grid[7][5] = "S"
        Grid[8][4] = "I"
        Grid[8][7] = "I"
        Grid[9][4] = "R"
        chosenTiles = ["A","S","K"]
    elif testNumber == 5:
        Grid[0][0] = "K"
        Grid[0][1] = "A"
        Grid[0][2] = "L"
        Grid[3][0] = "K"
        Grid[3][1] = "A"
        Grid[3][2] = "L"
        chosenTiles = ["E"]
    elif testNumber == 6:
        Grid[0][0] = "G"
        Grid[0][1] = "R"
        Grid[0][2] = "E"
        Grid[0][3] = "A"
        Grid[0][4] = "T"
        Grid[1][4] = "E"
        Grid[2][4] = "R"
        Grid[3][4] = "R"
        Grid[4][4] = "I"
        Grid[5][4] = "B"
        Grid[6][4] = "L"
        Grid[7][4] = "E"
        Grid[3][2] = "A"
        Grid[3][3] = "L"
        Grid[3][5] = "I"
        Grid[3][6] = "G"
        Grid[3][7] = "H"
        Grid[3][8] = "T"
        chosenTiles = ["_","_","Q"]
    print findBothSolutions(Grid,chosenTiles,True)
