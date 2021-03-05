#This file is responsible for the actual working of the game

import pygame as p
from ChessEngine import GameState

WIDTH = HEIGHT = 512
DIMENSION = 8 #The dimensions of the board is 8x8
SQ_SIZE = HEIGHT//DIMENSION #Each sqaure of the board has this size (i.e 64 squares total)
MAX_FPS = 15# For animations
IMAGES = {}

#Initialize a global dictionary of images. This will be called exactly once in main

def loadImages():
    pieces = ['wR','wQ','wp','wN','wK','wB','bR','bQ','bp','bN','bK','bB'] #Using pygame to load up the images of each piece
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load('Images/' + piece + '.png'), (SQ_SIZE,SQ_SIZE))


#The main driver for the program. This handles user input + updating the graphics.

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock = p.time.Clock() #Helps to control the games framerate
    screen.fill(p.Color("white"))
    gs = GameState() 
    loadImages() #We only load the images once, that too before the while loop
    running = True
    while running:
        for e in p.event.get(): #This line of code goes through the event queue, i.e, all the event calls that happen like mouse clicks, button presses etc.
            if e.type == p.QUIT:
                running = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()


#Responsible for all the graphics in the current game state.

def drawGameState(screen, gs):
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) #draw pieces on top of the squares


#Draw the squares on the board
def drawBoard(screen):
    # colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if (r+c)%2 == 0: #All 0 remainders are white
               color = p.Color(235, 235, 208)
               p.draw.rect(screen , color , p.Rect(c*SQ_SIZE , r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) 
            else: #All non 0 remainders are black
               color = p.Color(119, 148, 85)
               p.draw.rect(screen , color , p.Rect(c*SQ_SIZE , r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


                
    
#draw pieces on top of the squares using the GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #Not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE , r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
  



if __name__ == "__main__":
    main()


