import pygame
import sys
import time
import math
import random
import json
import copy
import threading
from datetime import datetime

from database import (register_user, login_user, get_user, update_elo,
                      save_game, get_user_games, get_leaderboard,
                      calculate_elo_change)
from engine import (ChessGame, get_computer_move, WHITE, BLACK,
                    PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING, EMPTY)
from ui import (W, H, C, BOARD_THEMES, BOARD_SIZE, SQUARE, BOARD_X, BOARD_Y,
                draw_rounded_rect, draw_glow, draw_gradient_rect,
                lerp_color, Button, InputField)
from pieces import get_piece_surface

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("ChessMaster Pro")
clock = pygame.time.Clock()