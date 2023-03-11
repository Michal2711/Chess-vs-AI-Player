from copy import deepcopy
import pygame
# from alg import get_all_moves
from constants import BROWN, GOLD, WHITE, SQUARE_SIZE, GREEN, RED
from constants import Black_King, White_King
from board import Board
# from PIL import Image, ImageFilter
# from check_mat import if_mat


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.board.draw(self.win)
        self.check = False
        self.check_check_mat = False
        self.result = None

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if self.check is True:
            self.draw_check()
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        # BROWN
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            # if self.coercion(piece.color) is True and [] in self.valid_moves.values():
            #     self.valid_moves = {}
            return True

        return False

    def _move(self, row, col):
        if self.selected and (row, col) in self.valid_moves:
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped[0])
            self.board.move(self.selected, row, col)
            self.check = self.board.check_check(self.turn)
            if self.check is True:
                self.check_check_mat = self.board.check_mat(self.turn, self.get_all_moves)
                if self.check_check_mat is True:
                    print("mat")
                    pygame.time.delay(1000)
                    self.winner()
                else:
                    print("szach")
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                GREEN,
                (
                    col * SQUARE_SIZE + SQUARE_SIZE//2,
                    row * SQUARE_SIZE + SQUARE_SIZE//2),
                15
            )

    def draw_check(self):
        for i in range(0, 8, 1):
            for j in range(0, 8, 1):
                if self.board.board[i][j] != 0:
                    current = self.board.board[i][j]
                    if current.color == self.turn and current.figure == 'King':
                        row = current.row
                        col = current.col
                        if self.check_check_mat is True:
                            pygame.draw.rect(self.win, GOLD, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        else:
                            pygame.draw.rect(self.win, RED, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                        if self.turn == WHITE:
                            current.draw_blit(self.win, White_King)
                        else:
                            current.draw_blit(self.win, Black_King)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BROWN:
            self.turn = WHITE
        else:
            self.turn = BROWN

    def get_board(self):
        return self.board

    def get_all_moves(self, board, color):
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = self.board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                # self.draw_moves(board, piece)
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)
        return moves

    def simulate_move(self, piece, move, board, skip):
        if skip:
            # print(skip)
            board.remove(skip)
        board.move(piece, move[0], move[1])
        return board

    def draw_moves(self, board, piece):
        valid_moves = board.get_valid_moves(piece)
        board.draw(self.win)
        pygame.draw.circle(self.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
        self.draw_valid_moves(valid_moves.keys())
        pygame.display.update()
        pygame.time.delay(100)

    def winner(self):
        if self.turn == WHITE:
            self.result = "WHITE WON"
        else:
            self.result = "BROWN WON"
        # self.fade(WIDTH, HEIGHT)
        # pygame.time.delay(500)

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def fade(self, width, height):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        for alpha in range(0, 150):
            fade.set_alpha(alpha)
            # self.win.fill((255, 255, 255))
            self.win.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
