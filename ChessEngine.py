#This file stores all the current data about the game. It will keep a move log and determine the valid moves.

class GameState():
    def __init__(self):
        self.board = [   
            ["bR","bN","bB","bQ","bK","bB", "bN", "bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"], #Corrected the positioning of the pieces
            ["wR","wN","wB","wQ","wK","wB", "wN", "wR"]            
        ]

        self.whiteToMove = True #To check whose turn it is
        self.moveLog = [] 

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Log the move so we can undo it later or if we want to display the history of the game
        self.whiteToMove = not self.whiteToMove #switch turns

class Move():
    #maps keys to values
    # keys : values
    rank = 7
    ranksToRows = dict()
    for i in range(1,9):
        ranksToRows[str(i)] = rank
        rank-=1 
    rowsToRanks = {v: k for k, v in ranksToRows.items()} 

    file = "a"
    filesToCols = dict()
    for i in range(0,8):
        filesToCols[file] = i
        file = ord(file)
        file += 1
        file = chr(file)
    colsToFiles = {v: k for k, v in filesToCols.items()}



    def __init__(self, startSq, endSq, board): #We store the board as well in order to see if a piece is being captured, which piece it is and how to make it disappear. Also, in case we undo the move, we need to store that too.
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)


    def getRankFile(self,r,c): #Helper function to return a string of the File followed by the Rank
        return self.colsToFiles[c] + self.rowsToRanks[r]