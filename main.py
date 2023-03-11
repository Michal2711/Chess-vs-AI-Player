import argparse
import pygame
import sys
from constants import WIDTH, HEIGHT, SQUARE_SIZE, BROWN
from game import Game
from alg import minimax
# from alphabeta import alphabeta
# from board import Board

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('CHESS')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main(arguments):
    parser = argparse.ArgumentParser()
    parser.add_argument('--Player-vs-Player', action='store_true')
    parser.add_argument('--vs-AI', action='store_true')

    args = parser.parse_args(arguments[1:])

    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if args.vs_AI:
            if game.turn == BROWN:
                pygame.time.delay(1000)
                value, new_board = minimax(game.get_board(), 3, BROWN, game)
                # value, new_board = alphabeta(game.get_board(), 3, BROWN, game, float('-inf'), float('inf'))
                game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        if game.result is not None:
            print(game.result)
            game.update()
            pygame.time.delay(5000)
            # game.fade(WIDTH, HEIGHT)
            run = False

        if run is True:
            game.update()
    pygame.quit()


if __name__ == "__main__":
    main(sys.argv)
