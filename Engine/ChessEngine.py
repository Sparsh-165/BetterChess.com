"""
This is responsible for the representation of the chess board. Also it will determine if the move is a valid move or not
"""


from numpy.matlib import piecewise


class GameState():
    def __init__(self):# This is the representation of the chess board, the first char represents the color of the piece, the second char represents the type of the piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []


    '''
    Takes a move as a parameter and executes it (this will not work for castling, en passant, or pawn promotion)
    '''
    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move) # we log the move to later display or use it for AI
        self.white_to_move = not self.white_to_move # swap turns 

    '''
    This will undo the last move made by the user
    '''


    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move # switch turn 
        else:
            print("No moves to undo")


    '''
    All moves considering checks
    '''

    def get_valid_moves(self):
        pass

    '''
    All moves without considering checks
    '''

    def get_all_possible_moves(self):
        pass

class Move():

    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}



    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_column = start_sq[1]
        self.end_row = end_sq[0]
        self.end_column = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]


    def get_chess_notation(self):
        #you can add this to make this a real chess notation
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)
        
    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]