import pygame
from constants import SQUARE_SIZE, WHITE, BROWN
from constants import (
    Black_King, White_King,
    Black_Queen, White_Queen,
    Black_Tower, White_Tower,
    Black_Bishop, White_Bishop,
    Black_Knight, White_Knight,
    Black_Pawn, White_Pawn
)


class Piece:
    def __init__(self, row, col, color, figure):
        self.row = row
        self.col = col
        self.color = color
        self.figure = figure

        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw(self, win):
        if self.figure == 'King' and self.color == BROWN:
            self.draw_blit(win, Black_King)
        elif self.figure == 'King' and self.color == WHITE:
            self.draw_blit(win, White_King)
        elif self.figure == 'Queen' and self.color == BROWN:
            self.draw_blit(win, Black_Queen)
        elif self.figure == 'Queen' and self.color == WHITE:
            self.draw_blit(win, White_Queen)
        elif self.figure == 'Tower' and self.color == BROWN:
            self.draw_blit(win, Black_Tower)
        elif self.figure == 'Tower' and self.color == WHITE:
            self.draw_blit(win, White_Tower)
        elif self.figure == 'Bishop' and self.color == BROWN:
            self.draw_blit(win, Black_Bishop)
        elif self.figure == 'Bishop' and self.color == WHITE:
            self.draw_blit(win, White_Bishop)
        elif self.figure == 'Knight' and self.color == BROWN:
            self.draw_blit(win, Black_Knight)
        elif self.figure == 'Knight' and self.color == WHITE:
            self.draw_blit(win, White_Knight)
        elif self.figure == 'Pawn' and self.color == BROWN:
            self.draw_blit(win, Black_Pawn)
        elif self.figure == 'Pawn' and self.color == WHITE:
            self.draw_blit(win, White_Pawn)

    def draw_blit(self, win, Figure):
        win.blit(
            Figure,
            (
                self.x - Figure.get_width()//2,
                self.y - Figure.get_height()//2
            )
        )

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(f'{self.figure}')
