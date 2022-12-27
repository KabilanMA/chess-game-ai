
from const import *
from square import Square
from piece import *
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_piece('white')
        self._add_piece('black')
    
    def move(self, piece:Piece, move: Move):
        initial = move.initial
        final = move.final

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # move
        piece.moved = True

        # clear valid moves
        piece.clear_moves()

        # set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves



    def calc_moves(self, piece:Piece, row:int, col:int):
        '''
            Calculate all the possible valid moves of a specific piece on a specific position
        '''

        '''get the possible moves of the knight on the board'''
        def knight_moves():
            # 8 possbile move for a knight
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row-2, col-1),
                (row-1, col-2),
                (row+1, col-2),
                (row+2, col-1),
                (row+2, col+1)
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create the sqaures of the new moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create a new move
                        move = Move(initial, final)

                        # append new valid move
                        piece.add_move(move)
        

        '''get the possible moves of the knight on the board'''
        def pawn_moves():
            steps = 1 if piece.moved else 2
            piece.moved = True

            # vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1+ steps))

            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        # create initial and final move sqaures
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    
                    # blocked by other piece to move
                    else:
                        break
                # if a position is not in range then other preceding moves will not be in range
                else:
                    break

            # diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]

            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        # create initial and final move sqaures
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a new move
                        move = Move(initial, final)
                        piece.add_move(move)

        def straightline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create the sqaures of the new moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a possbile new move
                        move = Move(initial, final)

                        # empty -> continue looping
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # create a new move
                            piece.add_move(move)

                        # has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # create a new move
                            piece.add_move(move)
                            # can't move over one piece
                            break
                        
                        # has team piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            # can't move over one piece
                            break

                    # not in the board range
                    else:
                        break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [
                (row-1,col), # up
                (row+1,col+0), # down
                (row,col+1), # right
                (row,col-1), # left
                (row-1,col+1), # up-right
                (row-1,col-1), # up-left
                (row+1,col+1), # down-right
                (row+1,col-1) # down-left
            ]

            # normal moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        # create the squares of the new moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        # create a new move
                        move = Move(initial, final)

                        # append new valid move
                        piece.add_move(move)
            
            # castling moves

            # queen castling

            # king castling


        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece, Knight): knight_moves()

        elif isinstance(piece, Bishop): straightline_moves([
            (-1, 1), # up-right
            (-1, -1), # up-left
            (1,1), # down-right
            (1, -1) # down-left
        ])

        elif isinstance(piece, Rook): straightline_moves([
            (-1, 0), # up
            (0, 1), # right
            (1, 0), # down
            (0, -1) # left
        ])

        elif isinstance(piece, Queen): straightline_moves([
            (-1, 1), # up-right
            (-1, -1), # up-left
            (1,1), # down-right
            (1, -1), # down-left
            (-1, 0), # up
            (0, 1), # right
            (1, 0), # down
            (0, -1) # left
        ])

        elif isinstance(piece, King): king_moves()

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
        # print(self.squares)

    def _add_piece(self, color):
        if color == 'white':
            row_pawn, row_other = (6,7)
        else:
            row_pawn, row_other = (1,0)

        # put pawn on the board
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        
        # self.squares[5][2] = Square(5, 2, Pawn(color))

        
        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        # self.squares[2][3] = Square(2, 3, King(color))


b = Board()
b._create()
