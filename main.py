'''
This is a driver file . This will be used to take the user input and display the board
'''


from sqlite3.dbapi2 import sqlite_version
from this import s
from tomllib import load
from unittest import runner

from numpy import piecewise
from numpy.random.mtrand import sample
import pygame as p
from pygame.display import gl_set_attribute
from Engine import ChessEngine


WIDTH = HEIGHT = 512 # 400 is also a good size
DIMENSIONS = 8 #chess board is 8x8
SQ_SIZE = WIDTH // DIMENSIONS
MAX_FPS = 15 # for animation later on
IMAGES = {}

'''
Initailize a global dictionary of images. This will be initialized once and then reused.
'''


def load_images():
    piece_names = ["wP", "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in piece_names:
        IMAGES[piece] = p.transform.scale(p.image.load("Assests/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


'''
This is going to be the main driver and handle all the user input .
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    sq_selected = () #No square is selected initially, This will keep track of last mouse click location tuple:(row, col)
    player_clicks = [] # keeps track of player clicks, two tuples per click: (start_row, start_col) and (end_row, end_col)
    print(gs.board)
    load_images() # Only loading this once, before the while loop.
    print(IMAGES.keys())
    running = True
    while running:
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            #mouse handlers 
            elif event.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #This is the x&y coordinates of the mouse
                print(location)
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                print(col, row)
                if sq_selected == (row, col):# The user has selected the same square, deselect it
                    sq_selected = () # Deselect the square
                    player_clicks = [] # Clear the player clicks
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected) # we append the first and second clicks of the player and save it in the player_clicks list

                if len(player_clicks) == 2: # After 2nd click
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = ()  # reset our clicks
                    player_clicks = []
                    
            # key handlers
            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:# when "z" is pressed
                    gs.undo_move()

        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


'''
This function draws the board and pieces on the screen. Responsible for all the graphic within a current game state
'''
def draw_game_state(screen, gs):
    draw_board(screen)# Draw sqaure in board
    #Add in pieces and highlight or move suggestion (later)
    draw_pieces(screen, gs.board)#draw pieces on that squares


'''
This function is here to draw all the squares on the board. In chess boards, the top left square is always white, so the board is drawn with alternating colors.
'''
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[(row + col) % 2]
            p.draw.rect(screen, color, p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))



'''
This function is here to draw all the pieces on the board. The order is important, so the pieces are drawn in order from top to bottom, left to right.
We also put the piece on the draw_board function so the pieces are drawn on top of the board.
This will only be called when the board is drawn and it will be called only once.
'''
def draw_pieces(screen, board):
    for row in range(DIMENSIONS):
        for column in range(DIMENSIONS):
            piece = board[row][column]
            if piece != "--":#Not empty string
                screen.blit(IMAGES[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))





if __name__ == "__main__":
    main()
