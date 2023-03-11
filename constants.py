import pygame

# szerokość okna gry, ilość rzędów i kolumn, rozmiary jednego pola na planszy
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# kolory zapisane w formacie RGB
BROWN = (102, 51, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
BROWN2 = (67, 48, 5)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (187, 161, 79)

Black_King = pygame.transform.scale(pygame.image.load('pieces/black_king.png'), (100, 100))
Black_Queen = pygame.transform.scale(pygame.image.load('pieces/black_queen.png'), (100, 100))
Black_Tower = pygame.transform.scale(pygame.image.load('pieces/black_tower.png'), (100, 100))
Black_Bishop = pygame.transform.scale(pygame.image.load('pieces/black_bishop.png'), (100, 100))
Black_Knight = pygame.transform.scale(pygame.image.load('pieces/black_knight.png'), (100, 100))
Black_Pawn = pygame.transform.scale(pygame.image.load('pieces/black_pawn.png'), (100, 100))
White_King = pygame.transform.scale(pygame.image.load('pieces/white_king.png'), (100, 100))
White_Queen = pygame.transform.scale(pygame.image.load('pieces/white_queen.png'), (100, 100))
White_Tower = pygame.transform.scale(pygame.image.load('pieces/white_tower.png'), (100, 100))
White_Bishop = pygame.transform.scale(pygame.image.load('pieces/white_bishop.png'), (100, 100))
White_Knight = pygame.transform.scale(pygame.image.load('pieces/white_knight.png'), (100, 100))
White_Pawn = pygame.transform.scale(pygame.image.load('pieces/white_pawn.png'), (100, 100))
