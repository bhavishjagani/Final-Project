import pygame
pygame.init()
 
WINDOW_WIDTH  = 1060
WINDOW_HEIGHT = 780
SQUARE_SIZE   = 76
BOARD_OFFSET_X = 120
BOARD_OFFSET_Y = (WINDOW_HEIGHT - SQUARE_SIZE * 8) // 2
 
COLOR_SQUARE_LIGHT = (235, 211, 174)
COLOR_SQUARE_DARK = (165, 117, 74)
COLOR_BACKGROUND = (18, 16, 22)
COLOR_PANEL = (26, 24, 32)
COLOR_CARD = (34, 32, 42)
COLOR_ACCENT = (252, 196, 68)
COLOR_TEXT = (230, 225, 215)
COLOR_DIM = (110, 105, 120)
COLOR_DANGER = (210, 55, 55)
COLOR_SELECTION = (100, 200, 80)
COLOR_CHECK = (220, 50, 50)
COLOR_BORDER = (50, 48, 62)
COLOR_WHITE_PIECE = (245, 240, 228)
COLOR_BLACK_PIECE = (38, 34, 28)
COLOR_WHITE_OUTLINE = (80, 68, 50)
COLOR_BLACK_OUTLINE = (210, 195, 168)
 
try:
    FONT_LARGE  = pygame.font.SysFont("georgia", 44, bold=True)
    FONT_MEDIUM = pygame.font.SysFont("georgia", 26, bold=True)
    FONT_SMALL  = pygame.font.SysFont("helvetica", 17)
    FONT_TINY   = pygame.font.SysFont("helvetica", 13)
except:
    FONT_LARGE  = pygame.font.SysFont(None, 44, bold=True)
    FONT_MEDIUM = pygame.font.SysFont(None, 26, bold=True)
    FONT_SMALL  = pygame.font.SysFont(None, 17)
    FONT_TINY   = pygame.font.SysFont(None, 13)
 
INITIAL_BOARD = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"], ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
    [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None],
    ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"], ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],]