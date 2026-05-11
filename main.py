import pygame
import sys

pygame.init()

W, H = 800, 800
SQUARE = 80
BOARD_SIZE = SQUARE * 8
BOARD_X = (W - BOARD_SIZE) // 2
BOARD_Y = (H - BOARD_SIZE) // 2

LIGHT = (240, 217, 181)
DARK  = (181, 136,  99) 

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("ChessMaster")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 20, 15))

    for row in range(8):
        for col in range(8):
            color = LIGHT if (row + col) % 2 == 0 else DARK
            x = BOARD_X + col * SQUARE
            y = BOARD_Y + row * SQUARE
            pygame.draw.rect(screen, color, (x, y, SQUARE, SQUARE))

    pygame.display.flip()
    clock.tick(59)