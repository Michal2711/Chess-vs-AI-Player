import pygame
import random
# from alg import get_all_moves
# from game import get_all_moves
from constants import ROWS, SQUARE_SIZE, COLS, WHITE, BROWN, BROWN2
from piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.brown_king = self.white_king = 1
        self.create_board()
        self.white_left_castling = True
        self.white_right_castling = True
        self.black_left_castling = True
        self.black_right_castling = True
        self.check = False
        self.check_check_mat = False

    def draw_squares(self, win):
        win.fill(BROWN2)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def check_check(self, turn) -> bool:
        pieces = self.get_all_pieces(turn)
        self.check = False
        for piece in pieces:
            moves = self.get_valid_moves(piece)
            for move in moves.values():
                if move != []:
                    if move[0].figure == 'King':
                        self.check = True
                        return True
        return False

    def check_mat(self, turn, get_all_moves) -> bool:
        color = WHITE if turn == BROWN else BROWN
        # print(get_all_moves(self, color))
        for move in get_all_moves(self, color):
            mat_check = self.if_check(move, turn)
            if mat_check is False:
                self.check_check_mat = False
                return False
        self.check_check_mat = True
        return True

    def if_check(self, board, color):
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                if skip != [] and skip[0].figure == 'King':
                    return True
        return False

    def evaluate(self, board, turn, get_all_moves):
        result = 0
        # check = game.check
        if board.check is True:
            mat = board.check_mat(turn, get_all_moves)
            if mat is True:
                if turn == WHITE:
                    return 9999
                else:
                    return -9999
            else:
                if turn == WHITE:
                    return 300
                else:
                    return -300
        result = random.random()
        # print(result)
        return result

    def move(self, piece, row, col):
        if piece != 0:
            self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        if self.board[0][0] == 0 or self.board[0][4] == 0:
            self.black_left_castling = False
        if self.board[0][7] == 0 or self.board[0][4] == 0:
            self.black_right_castling = False
        if self.board[7][0] == 0 or self.board[7][4] == 0:
            self.white_left_castling = False
        if self.board[7][7] == 0 or self.board[7][4] == 0:
            self.white_right_castling = False
        if piece != 0:
            if piece.figure == "King" and abs(piece.col - col) not in (0, 1):
                if col == 2 and (row == 7 or row == 0):
                    Tower = self.get_piece(row, col - 2)
                    tower_col = Tower.col + 3
                elif col == 6 and (row == 7 or row == 0):
                    Tower = self.get_piece(row, col + 1)
                    tower_col = Tower.col - 2
                self.board[Tower.row][Tower.col], self.board[row][tower_col] = self.board[row][tower_col], self.board[Tower.row][Tower.col]
                Tower.move(row, tower_col)
            piece.move(row, col)

            if piece.figure == "Pawn" and (row == ROWS - 1 or row == 0):
                piece.figure = input("podaj figure na jaką zamienić: ")

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row == 0:
                    if col == 0 or col == (COLS - 1):
                        self.board[row].append(Piece(row, col, BROWN, 'Tower'))
                    elif col == 1 or col == (COLS - 2):
                        self.board[row].append(Piece(row, col, BROWN, 'Knight'))
                    elif col == 2 or col == (COLS - 3):
                        self.board[row].append(Piece(row, col, BROWN, 'Bishop'))
                    elif col == 3:
                        self.board[row].append(Piece(row, col, BROWN, 'Queen'))
                    else:
                        self.board[row].append(Piece(row, col, BROWN, 'King'))
                elif row == 1:
                    self.board[row].append(Piece(row, col, BROWN, 'Pawn'))
                elif row == (ROWS - 2):
                    self.board[row].append(Piece(row, col, WHITE, 'Pawn'))
                elif row == (ROWS - 1):
                    if col == 0 or col == (COLS - 1):
                        self.board[row].append(Piece(row, col, WHITE, 'Tower'))
                    elif col == 1 or col == (COLS - 2):
                        self.board[row].append(Piece(row, col, WHITE, 'Knight'))
                    elif col == 2 or col == (COLS - 3):
                        self.board[row].append(Piece(row, col, WHITE, 'Bishop'))
                    elif col == 4:
                        self.board[row].append(Piece(row, col, WHITE, 'King'))
                    else:
                        self.board[row].append(Piece(row, col, WHITE, 'Queen'))
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, piece):
        try:
            self.board[piece.row][piece.col] = 0
        except AttributeError:
            self.board[piece[0].row][piece[0].col] = 0

    def get_valid_moves(self, piece):
        moves = {}
        row = piece.row
        col = piece.col
        figure = piece.figure
        color = piece.color

        if figure == 'Pawn':
            if piece.color == WHITE:
                moves.update(self._go_up_once(row, col, color, figure))
                moves.update(self._go_right_up(row, col, color, figure))
                moves.update(self._go_left_up(row, col, color, figure))
            else:
                moves.update(self._go_down_once(row, col, color, figure))
                moves.update(self._go_right_down(row, col, color, figure))
                moves.update(self._go_left_down(row, col, color, figure))
        elif figure == 'Tower':
            moves.update(self._go_up(row, col, color))
            moves.update(self._go_down(row, col, color))
            moves.update(self._go_left(row, col, color))
            moves.update(self._go_right(row, col, color))
        elif figure == 'Bishop':
            moves.update(self._go_right_up(row, col, color, figure))
            moves.update(self._go_right_down(row, col, color, figure))
            moves.update(self._go_left_up(row, col, color, figure))
            moves.update(self._go_left_down(row, col, color, figure))
        elif figure == 'Queen':
            moves.update(self._go_up(row, col, color))
            moves.update(self._go_left(row, col, color))
            moves.update(self._go_right(row, col, color))
            moves.update(self._go_down(row, col, color))
            moves.update(self._go_right_up(row, col, color, figure))
            moves.update(self._go_right_down(row, col, color, figure))
            moves.update(self._go_left_up(row, col, color, figure))
            moves.update(self._go_left_down(row, col, color, figure))
        elif figure == 'King':
            moves.update(self._go_up_once(row, col, color, figure))
            moves.update(self._go_down_once(row, col, color, figure))
            moves.update(self._go_right_once(row, col, color))
            moves.update(self._go_left_once(row, col, color))
            moves.update(self._go_right_up(row, col, color, figure))
            moves.update(self._go_right_down(row, col, color, figure))
            moves.update(self._go_left_up(row, col, color, figure))
            moves.update(self._go_left_down(row, col, color, figure))
            if row == 7 and color == WHITE and (self.white_left_castling or self.white_right_castling):
                moves.update(self.White_castling(piece))
            elif row == 0 and color == BROWN and (self.black_left_castling or self.black_right_castling):
                moves.update(self.Black_castling(piece))
        elif figure == 'Knight':
            moves.update(self._go_knight(row, col, color))
        return moves

    def _go_up_once(self, row, col, color, figure):
        moves = {}
        if row - 1 == -1:
            return {}
        current = self.board[row-1][col]
        if figure == 'Pawn':
            if current == 0:
                moves[(row - 1, col)] = []
                current = self.board[row-2][col]
                if current == 0 and row == 6:
                    moves[(row - 2, col)] = []
            return moves
        else:
            if current == 0:
                moves[(row - 1, col)] = []
                return moves
            else:
                if current.color != color:
                    moves[(row - 1, col)] = [current]
                    return moves
                else:
                    return moves

    def _go_down_once(self, row, col, color, figure):
        moves = {}
        if row + 1 == 8:
            return {}
        current = self.board[row+1][col]
        if figure == 'Pawn':
            if current == 0:
                moves[(row + 1, col)] = []
                current = self.board[row+2][col]
                if current == 0 and row == 1:
                    moves[(row + 2, col)] = []
            return moves
        else:
            if current == 0:
                moves[(row + 1, col)] = []
                return moves
            else:
                if current.color != color:
                    moves[(row + 1, col)] = [current]
                    return moves
                else:
                    return moves

    def _go_right_once(self, row, col, color):
        moves = {}
        if col + 1 == 8:
            return {}
        current = self.board[row][col+1]
        if current == 0:
            moves[(row, col + 1)] = []
            return moves
        elif current.color != color:
            moves[(row, col + 1)] = [current]
            return moves
        else:
            return moves

    def _go_left_once(self, row, col, color):
        moves = {}
        if col - 1 == 0:
            return {}
        current = self.board[row][col-1]
        if current == 0:
            moves[(row, col - 1)] = []
            return moves
        elif current.color != color:
            moves[(row, col - 1)] = [current]
            return moves
        else:
            return moves

    def _go_up(self, row, col, color):
        moves = {}
        if row - 1 < 0:
            return moves
        else:
            row -= 1
        current = self.board[row][col]
        if current == 0:
            moves[(row, col)] = []
        elif current.color != color:
            moves[(row, col)] = [current]
            return moves
        else:
            return moves
        moves.update(self._go_up(row, col, color))
        return moves

    def _go_down(self, row, col, color):
        moves = {}
        if row + 1 > 7:
            return moves
        else:
            row += 1
        current = self.board[row][col]
        if current == 0:
            moves[(row, col)] = []
        elif current.color != color:
            moves[(row, col)] = [current]
            return moves
        else:
            return moves
        moves.update(self._go_down(row, col, color))
        return moves

    def _go_left(self, row, col, color):
        moves = {}
        if col - 1 < 0:
            return moves
        else:
            col -= 1
        current = self.board[row][col]
        if current == 0:
            moves[(row, col)] = []
        elif current.color != color:
            moves[(row, col)] = [current]
            return moves
        else:
            return moves
        moves.update(self._go_left(row, col, color))
        return moves

    def _go_right(self, row, col, color):
        moves = {}
        if col + 1 > 7:
            return moves
        else:
            col += 1
        current = self.board[row][col]
        if current == 0:
            moves[(row, col)] = []
        elif current.color != color:
            moves[(row, col)] = [current]
            return moves
        else:
            return moves
        moves.update(self._go_right(row, col, color))
        return moves

    def _go_right_up(self, row, col, color, figure):
        moves = {}
        if row - 1 < 0 or col + 1 > 7:
            return moves
        else:
            row -= 1
            col += 1
            current = self.board[row][col]
            if figure != 'Pawn':
                if current == 0:
                    moves[(row, col)] = []
                    if figure == 'King':
                        return moves
                else:
                    if current.color != color:
                        moves[(row, col)] = [current]
                        return moves
                    else:
                        return moves
            else:
                if current != 0:
                    if current.color != color:
                        moves[(row, col)] = [current]
                return moves
        moves.update(self._go_right_up(row, col, color, figure))
        return moves

    def _go_right_down(self, row, col, color, figure):
        moves = {}
        if row + 1 > 7 or col + 1 > 7:
            return moves
        else:
            row += 1
            col += 1
            current = self.board[row][col]
            if figure != 'Pawn':
                if current == 0:
                    moves[(row, col)] = []
                    if figure == 'King':
                        return moves
                else:
                    if current.color != color:
                        moves[(row, col)] = [current]
                        return moves
                    else:
                        return moves
            else:
                if current != 0:
                    if current.color != color:
                        moves[(row, col)] = [current]
                return moves
        moves.update(self._go_right_down(row, col, color, figure))
        return moves

    def _go_left_up(self, row, col, color, figure):
        moves = {}
        if row - 1 < 0 or col - 1 < 0:
            return moves
        else:
            row -= 1
            col -= 1
            current = self.board[row][col]
            if figure != 'Pawn':
                if current == 0:
                    moves[(row, col)] = []
                    if figure == 'King':
                        return moves
                else:
                    if current.color != color:
                        moves[(row, col)] = [current]
                        return moves
                    else:
                        return moves
            else:
                if current != 0:
                    if current.color != color:
                        moves[(row, col)] = [current]
                return moves
        moves.update(self._go_left_up(row, col, color, figure))
        return moves

    def _go_left_down(self, row, col, color, figure):
        moves = {}
        if row + 1 > 7 or col - 1 < 0:
            return moves
        else:
            row += 1
            col -= 1
            current = self.board[row][col]
            if figure != 'Pawn':
                if current == 0:
                    moves[(row, col)] = []
                    if figure == 'King':
                        return moves
                else:
                    if current.color != color:
                        moves[(row, col)] = [current]
                        return moves
                    else:
                        return moves
            else:
                if current != 0:
                    if current.color != color:
                        moves[(row, col)] = [current]
                return moves
        moves.update(self._go_left_down(row, col, color, figure))
        return moves

    def _go_knight(self, row, col, color):
        moves = {}
        if row - 2 >= 0 and col + 1 <= 7:
            current = self.board[row-2][col+1]
            if current == 0:
                moves[(row-2, col+1)] = []
            elif current.color != color:
                moves[(row-2, col+1)] = [current]
        if row - 1 >= 0 and col + 2 <= 7:
            current = self.board[row-1][col+2]
            if current == 0:
                moves[(row-1, col+2)] = []
            elif current.color != color:
                moves[(row-1, col+2)] = [current]
        if row + 1 <= 7 and col + 2 <= 7:
            current = self.board[row+1][col+2]
            if current == 0:
                moves[(row+1, col+2)] = []
            elif current.color != color:
                moves[(row+1, col+2)] = [current]
        if row + 2 <= 7 and col + 1 <= 7:
            current = self.board[row+2][col+1]
            if current == 0:
                moves[(row+2, col+1)] = []
            elif current.color != color:
                moves[(row+2, col+1)] = [current]
        if row + 2 <= 7 and col - 1 >= 0:
            current = self.board[row+2][col-1]
            if current == 0:
                moves[(row+2, col-1)] = []
            elif current.color != color:
                moves[(row+2, col-1)] = [current]
        if row + 1 <= 7 and col - 2 >= 0:
            current = self.board[row+1][col-2]
            if current == 0:
                moves[(row+1, col-2)] = []
            elif current.color != color:
                moves[(row+1, col-2)] = [current]
        if row - 1 >= 0 and col - 2 >= 0:
            current = self.board[row-1][col-2]
            if current == 0:
                moves[(row-1, col-2)] = []
            elif current.color != color:
                moves[(row-1, col-2)] = [current]
        if row - 2 >= 0 and col - 1 >= 0:
            current = self.board[row-2][col-1]
            if current == 0:
                moves[(row-2, col-1)] = []
            elif current.color != color:
                moves[(row-2, col-1)] = [current]
        return moves

    def White_castling(self, King):
        moves = {}
        if self.white_left_castling:
            if self.board[7][1] == self.board[7][2] == self.board[7][3] == 0 and self.board[7][0].figure == 'Tower':
                moves[(7, 2)] = []
        if self.board[7][7] != 0 and self.white_right_castling:
            if self.board[7][5] == self.board[7][6] == 0 and self.board[7][7].figure == 'Tower':
                moves[(7, 6)] = []
        return moves

    def Black_castling(self, King):
        moves = {}
        if self.black_left_castling:
            if self.board[0][1] == self.board[0][2] == self.board[0][3] == 0 and self.board[0][0].figure == 'Tower':
                moves[(0, 2)] = []
        if self.board[0][7] != 0 and self.black_right_castling:
            if self.board[0][5] == self.board[0][6] == 0 and self.board[0][7].figure == 'Tower':
                moves[(0, 6)] = []
        return moves