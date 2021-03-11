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

        self.moveFunctions = {'p' : self.getPawnMoves, 'R' : self.getRookMoves, 'Q' : self.getQueenMoves, 
                              'N' : self.getKnightMoves, 'B' : self.getBishopMoves, 'K' : self.getKingMoves}
        self.whiteToMove = True #To check whose turn it is
        self.moveLog = [] 

    
    #Takes a Move as a parameter and executes it. Does not handle pawn promotion, castling and en passant
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) #Log the move so we can undo it later or if we want to display the history of the game
        self.whiteToMove = not self.whiteToMove #switch turns

    #Undo the last move made
    def undoMove(self):
        if len(self.moveLog) != 0 : #Checking if there's any moves to undo
            move = self.moveLog.pop()                
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    #All moves considering checks
    def getValidMoves(self):
        return self.getAllPossibleMoves()
                                                                        #We generate all the possible moves using the function below.
                                                                        #Then we validate the moves using the function above
    #All moves not considering checks 
    def getAllPossibleMoves(self):
        moves = [] 
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0] #We take the first character of the string. If it is 'w', we calculate whites moves. If it is 'b', we calculate blacks moves.
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1] #Second character of the string
                    self.moveFunctions[piece](r,c,moves) #Initially we had if statements. Now we created a dictionary to simplify the process of calling the respective function.
        return moves
    
    # Get all the pawn moves for the pawn located at the row , column and add these moves to the list
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove: #That is, white's turn to move
            if self.board[r-1][c] == "--": #1 square pawn advance
                moves.append(Move((r,c), (r-1,c), self.board))
                if r == 6 and self.board[r-2][c] == "--": #For two square pawn advance in the beginning of the game
                    moves.append(Move((r,c), (r-2,c), self.board))     
            if (c-1) >= 0: #To prevent going off the left of the board
                if self.board[r-1][c-1][0] == "b": #Enemy piece to capture
                    moves.append(Move((r,c), (r-1,c-1), self.board))
            if (c+1) <= 7: #To prevent going off the right
                if self.board[r-1][c+1][0] == "b": #Enemy piece to capture
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1,c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    moves.append(Move((r,c), (r+2,c), self.board))
            
            if (c-1) >= 0:
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r,c) , (r+1,c-1), self.board))
            if (c+1) <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1,c+1), self.board))       

            #Still need to add pawn promotions         


    # Get all the rook moves for the rook located at the row , column and add these moves to the list
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0) , (0,-1), (1,0), (0,1)) #Up, left, down and right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i #that is, starting location +(whatever direction it moves in * i)
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #empty space valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:       #enemey piece valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else:
                        break #Friendly piece invalid
                else:
                    break # off the board    


    def getKnightMoves(self,r,c,moves):
        directions = ((-2,-1), (-2,1), (-1,-2), (-1,2), (1,-2), (1,2), (2,-1), (2,1))
        allyColor = 'w' if self.whiteToMove else 'b'
        for m in directions:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #It is an enemy piece
                    moves.append(Move((r,c), (endRow,endCol), self.board))



    def getKingMoves(self,r,c,moves):
        directions = ((-1,-1), (1,-1), (-1,1), (1,1), (-1,0) , (0,-1), (1,0), (0,1)) 
        allyColor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #empty space valid
                    moves.append(Move((r,c), (endRow,endCol), self.board))
                

    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1) , (1,-1), (-1,1), (1,1)) #North-West diagonal, South-West, North-East, South-East   
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i #that is, starting location +(whatever direction it moves in * i)
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--': #empty space valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                    elif endPiece[0] == enemyColor:       #enemey piece valid
                        moves.append(Move((r,c), (endRow,endCol), self.board))
                        break
                    else:
                        break #Friendly piece invalid
                else:
                    break # off the board       

    def getQueenMoves(self,r,c,moves):
        self.getBishopMoves(r,c,moves)
        self.getRookMoves(r,c,moves)

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
        self.moveID = self.startRow * 1000 + self.startCol * 100 +  self.endRow * 10 + self.endCol  #An id for every move. Eg: 5455 means e4 to e5.

    #Overriding the equals method. We only use this because we use the Move class
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID == other.moveID
        return False

    
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)


    def getRankFile(self,r,c): #Helper function to return a string of the File followed by the Rank
        return self.colsToFiles[c] + self.rowsToRanks[r]