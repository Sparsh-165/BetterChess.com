"""
This is responsible for the representation of the chess board. Also it will determine if the move is a valid move or not
"""


from numpy.matlib import piecewise


class GameState():
    
    
    def __init__(self):
        # This is the representation of the chess board, the first char represents the color of the piece,
        #  the second char represents the type of the piece
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "bP", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.move_function = {
            'p' : self.get_pawn_moves,
            'R' : self.get_rook_moves,
            'N' : self.get_knight_moves,
            'B' : self.get_bishop_moves,
            'Q' : self.get_queen_moves,
            'K' : self.get_king_moves
        }
        # We have made a dictionary of called move_function, inside which we have mapped the each letter with its own method
        # Using this helps in removing the uncessary if else statement required for each move decision
        # We have to use this way of doing this because there is no 'switch' statement in python.
          
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
        return self.get_all_possible_moves() # for now there is no checks , it only returns the possible moves

    '''
    All moves without considering checks
    '''

    def get_all_possible_moves(self):
        moves = []
        for r in range(len(self.board)):# Number of Rows
            for c in range(len(self.board[r])): # Number of Columns
                turn = self.board[r][c][0]
                if (turn == 'w' and self.white_to_move) or (turn =='b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    # We can simply check what the piece selected is and check mapped method with it 
                    self.move_function[piece](r, c, moves) 
                    # Look in the constructor for explanation 
        return moves


    '''
    Get all the pawn moves for the pawn located at row, col and add these moves to the list
    '''

    def get_pawn_moves(self, r, c, moves):

        # White moves
        if self.white_to_move:
            if self.board[r-1][c] == '--': #This is one sqaure pawn advance
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--': #This is a 2 sqaure pawn advance
                    moves.append(Move((r,c), (r-2, c), self.board))

                    
            if c-1 >= 0 and self.board[r-1][c-1][0] == 'b': 
                moves.append(Move((r,c), (r-1,c-1), self.board))
                # These are capture check to the left a
                # Also to make it such that it doesn't capture from left side of the board to the right side of the board
                # if self.board[r-1][c-1][0] == 'b': # Check for enemy piece to capture to the left


                
            if c+1 <= 7 and self.board[r-1][c+1][0] == 'b':
                moves.append(Move((r,c), (r-1,c+1), self.board))
                # check of enemy piece to capture to the right
                # #captures to the right & we can also put len(self.board[r]) instead of 7
                # Combined both the if cases to together


        # black moves 
        else:
            if self.board[r+1][c] == '--':
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r + 2][c] == '--':
                    moves.append(Move((r,c), (r+2, c), self.board))


            # Black captures 
            if c+1 >= 0 and self.board[r + 1][c - 1][0] == 'w': #capture check to the left
                moves.append(Move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7 and self.board[r + 1][c + 1][0] == 'w':
                moves.append(Move((r, c), (r + 1, c + 1), self.board))

        # Pawn promotion is pending 
        # En Passant is pending
                
                 
                
            
                    

    '''
    Get all the rook moves for the Rook located at row, col, and add these moves to the list
    '''

    def get_rook_moves(self, r, c, moves):
        direction = ((-1, 0), (0,-1), (1, 0), (0, 1)) #Direction for rook -> up, left, down, right
        enemy_color = "b" if self.white_to_move else "w" # to set whether the enemy color is black or white using ternary operator 
        for d in direction:
            for i in range(1, 8):
                end_row = r + d[0]*i
                end_col = r + d[1]*i
                if 0 <= end_row < 8 and 0 <= end_col < 8: # check of being on the board
                    end_piece = self.board[end_row][end_col]
                    if end_piece == '--':
                        moves. append(Move((r,c), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color: # Enemy piece valid move
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break
                    else: # Friendly piece invalid move
                        break
                else: # off board
                    break

    '''
    Get all Knight moves for the knight located at row, Col and add these moves to the list
    '''

    def get_knight_moves(self, r, c, moves):
        pass


    '''
    GEt all Bishop moves for the knight loacted at row, col and add these moves to the list 
    '''

    def get_bishop_moves:(self, r, c, moves):
        
    


class Move():
    #This class is used to capture every move, its used again and again for  move generation


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
        self.move_ID = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column
        # print("~~~~")
        # print(self.move_ID)

    '''
    Overriding the equals method
    '''
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False


    def get_chess_notation(self):
        #you can add this to make this a real chess notation
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, row, col):
        return self.cols_to_files[col] + self.rows_to_ranks[row]
