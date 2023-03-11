from copy import deepcopy
import pygame
import random

BROWN = (102, 51, 0)
WHITE = (255, 255, 255)


# funkcja obslugująca ruch komputera, zwwraca nową planszę
def alphabeta(position, depth, max_player, game, alpha, beta):
    # position == game.board
    # if depth == 0 or position.winner(WHITE) is not None:
    # TUTAJ NIE WIEM CZY GAME JEST OK ALE MOZE ZADZIALA W RAZIE CZEGO SPRAWDZ
    if depth == 0:
        return position.evaluate(position, game, max_player), position

    if max_player == WHITE:
        # maxEval = float('-inf')
        best_move = None

        for move in get_all_moves(position, WHITE, game):
            evaluation = alphabeta(move, depth-1, BROWN, game, alpha, beta)[0]
            if alpha < evaluation:
                alpha = evaluation
                best_move = move
            if alpha >= beta:
                break
        return alpha, best_move
    else:
        # minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BROWN, game):
            evaluation = alphabeta(move, depth-1, WHITE, game, alpha, beta)[0]
            if beta > evaluation:
                beta = evaluation
                best_move = move
            if alpha >= beta:
                break
        return beta, best_move


# funkcja symuluje wykonanie przez komputer ruchu
def simulate_move(piece, move, board, game, skip):
    if skip:
        board.remove(skip)
    board.move(piece, move[0], move[1])
    return board


# funkcja zwracająca losowy ruch do wykonania
# wywołanie w pliku main.py jeśli chcielibyśmy aby komputer wykonywał losowe ruchy
def random_move(position, color, game):
    all_moves = get_all_moves(position, color, game)
    if all_moves:
        move = random.choice(all_moves)
    else:
        return None
    return move


# funkcja która dla wszystkich pionków danego koloru zwraca ich możliwe ruchy
def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        color = WHITE if game.turn == WHITE else BROWN
        # if game.coercion(color) is True and [] in valid_moves.values():
        #     valid_moves = {}
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    return moves


# funkcja która rysuję obramowanie dla pionka rozpatrywanego przez komputer
# pomocna dla sprawdzenia poprawności działania ruchu komputera
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)
