import pygame
from constants import (WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE, BOARD_OFFSET_X, BOARD_OFFSET_Y, COLOR_SQUARE_LIGHT, COLOR_SQUARE_DARK, COLOR_BACKGROUND, COLOR_PANEL, COLOR_CARD,
    COLOR_ACCENT, COLOR_TEXT, COLOR_DIM, COLOR_DANGER, COLOR_SELECTION, COLOR_CHECK, COLOR_BORDER, COLOR_WHITE_PIECE, COLOR_BLACK_PIECE, COLOR_WHITE_OUTLINE, COLOR_BLACK_OUTLINE, FONT_LARGE, FONT_MEDIUM, FONT_SMALL, FONT_TINY,)
 
def draw_text(surface, text, font, color, center_x, center_y, anchor="c"):
    rendered = font.render(str(text), True, color)
    rect = rendered.get_rect()
    if anchor == "c":
        rect.center = (center_x, center_y)
    elif anchor == "r":
        rect.midright = (center_x, center_y)
    elif anchor == "l":
        rect.midleft = (center_x, center_y)
    surface.blit(rendered, rect)
 
def draw_rounded_rect(surface, color, x, y, width, height, radius=8, border_width=0, border_color=None, alpha=None):
    if alpha is not None:
        temp = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(temp, (*color[:3], alpha), (0, 0, width, height), border_radius=radius)
        surface.blit(temp, (x, y))
        return
    pygame.draw.rect(surface, color, (x, y, width, height), border_radius=radius)
    if border_width and border_color:
        pygame.draw.rect(surface, border_color, (x, y, width, height), border_width, border_radius=radius)
 
class PieceRenderer:
    _surface_cache = {}
 
    @classmethod
    def get_surface(cls, piece, size):
        cache_key = (piece, size)
        if cache_key not in cls._surface_cache:
            cls._surface_cache[cache_key] = cls._build_surface(piece, size)
        return cls._surface_cache[cache_key]
 
    @classmethod
    def _build_surface(cls, piece, size):
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        piece_col = piece[0]
        piece_typ = piece[1:]
        fill_color = COLOR_WHITE_PIECE if piece_col == "w" else COLOR_BLACK_PIECE
        outline_color = COLOR_WHITE_OUTLINE if piece_col == "w" else COLOR_BLACK_OUTLINE
        center_x = size // 2
        center_y = size // 2
 
        def draw_circle(x, y, radius, fill, outline=None, line_width=2):
            if radius < 1:
                return
            pygame.draw.circle(surface, fill, (x, y), radius)
            if outline:
                pygame.draw.circle(surface, outline, (x, y), radius, line_width)
 
        def draw_polygon(points, fill, outline=None, line_width=2):
            if len(points) < 3:
                return
            pygame.draw.polygon(surface, fill, points)
            if outline:
                pygame.draw.polygon(surface, outline, points, line_width)
 
        def draw_box(x, y, width, height, fill, outline=None, corner_radius=3, line_width=2):
            rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
            pygame.draw.rect(surface, fill, rect, border_radius=corner_radius)
            if outline:
                pygame.draw.rect(surface, outline, rect, line_width, border_radius=corner_radius)
 
        if piece_typ == "P":
            base_width = int(size * 0.52)
            base_height = int(size * 0.18)
            neck_width = int(size * 0.28)
            head_radius = int(size * 0.22)
            base_y = int(center_y + size * 0.28)
            neck_y = int(center_y + size * 0.04)
            head_y = int(center_y - size * 0.12)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            neck_points = [(center_x - neck_width // 2, base_y - base_height // 2), (center_x + neck_width // 2, base_y - base_height // 2),
                (center_x + int(neck_width * 0.6), neck_y), (center_x - int(neck_width * 0.6), neck_y),]
            draw_polygon(neck_points, fill_color, outline_color)
            draw_circle(center_x, head_y, head_radius, fill_color, outline_color)
 
        elif piece_typ == "R":
            base_width  = int(size * 0.62)
            base_height = int(size * 0.16)
            body_width  = int(size * 0.48)
            body_height = int(size * 0.44)
            top_width   = int(size * 0.54)
            top_height  = int(size * 0.14)
            base_y  = int(center_y + size * 0.28)
            body_y = int(center_y + size * 0.00)
            top_y = int(center_y - size * 0.24)
            merlon_width = int(size * 0.13)
            merlon_height = int(size * 0.2)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            draw_box(center_x, body_y, body_width, body_height, fill_color, outline_color, corner_radius=3)
            draw_box(center_x, top_y, top_width, top_height, fill_color, outline_color, corner_radius=2)
            for offset_x in [-int(size * 0.17), 0, int(size * 0.17)]:
                draw_box(center_x + offset_x, top_y - merlon_height // 2, merlon_width, merlon_height, fill_color, outline_color, corner_radius=2)
 
        elif piece_typ == "N":
            base_width  = int(size * 0.60)
            base_height = int(size * 0.15)
            base_y      = int(center_y + size * 0.30)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            body_points = [
                (center_x - int(size * 0.22), base_y - base_height // 2),
                (center_x + int(size * 0.24), base_y - base_height // 2),
                (center_x + int(size * 0.26), int(center_y + size * 0.08)),
                (center_x + int(size * 0.34), int(center_y - size * 0.10)),
                (center_x + int(size * 0.30), int(center_y - size * 0.34)),
                (center_x + int(size * 0.08), int(center_y - size * 0.42)),
                (center_x - int(size * 0.14), int(center_y - size * 0.36)),
                (center_x - int(size * 0.28), int(center_y - size * 0.18)),
                (center_x - int(size * 0.24), int(center_y + size * 0.04)),
            ]
            draw_polygon(body_points, fill_color, outline_color)
            ear_points = [
                (center_x + int(size * 0.08), int(center_y - size * 0.42)),
                (center_x + int(size * 0.30), int(center_y - size * 0.34)),
                (center_x + int(size * 0.26), int(center_y - size * 0.18)),
                (center_x + int(size * 0.04), int(center_y - size * 0.24)),
            ]
            draw_polygon(ear_points, fill_color, outline_color)
            draw_circle(center_x + int(size * 0.16), int(center_y - size * 0.26), int(size * 0.06), outline_color)
            nostril_points = [
                (center_x - int(size * 0.14), int(center_y - size * 0.10)),
                (center_x - int(size * 0.02), int(center_y - size * 0.06)),
                (center_x - int(size * 0.04), int(center_y + size * 0.02)),
                (center_x - int(size * 0.18), int(center_y - size * 0.02)),
            ]
            draw_polygon(nostril_points, outline_color)
 
        elif piece_typ == "B":
            base_width = int(size * 0.60)
            base_height  = int(size * 0.15)
            collar_width = int(size * 0.42)
            collar_height = int(size * 0.12)
            base_y = int(center_y + size * 0.30)
            collar_y  = int(center_y + size * 0.14)
            head_radius = int(size * 0.18)
            head_y = int(center_y - size * 0.22)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            draw_box(center_x, collar_y, collar_width, collar_height, fill_color, outline_color, corner_radius=3)
            body_points = [
                (center_x - collar_width // 2, collar_y + collar_height // 2),
                (center_x + collar_width // 2, collar_y + collar_height // 2),
                (center_x + int(size * 0.14),  int(center_y - size * 0.16)),
                (center_x - int(size * 0.14),  int(center_y - size * 0.16)),
            ]
            draw_polygon(body_points, fill_color, outline_color)
            draw_circle(center_x, head_y, head_radius, fill_color, outline_color)
            draw_circle(center_x, int(center_y - size * 0.40), int(size * 0.06), outline_color)
            pygame.draw.line(surface, outline_color, (center_x - int(size * 0.12), int(center_y - size * 0.18)), (center_x + int(size * 0.12), int(center_y - size * 0.26)), 2,)
 
        elif piece_typ == "Q":
            base_width  = int(size * 0.64)
            base_height = int(size * 0.15)
            base_y      = int(center_y + size * 0.30)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            body_points = [
                (center_x - int(size * 0.28), base_y - base_height // 2),
                (center_x + int(size * 0.28), base_y - base_height // 2),
                (center_x + int(size * 0.20), int(center_y - size * 0.06)),
                (center_x - int(size * 0.20), int(center_y - size * 0.06)),
            ]
            draw_polygon(body_points, fill_color, outline_color)
            crown_points = [
                (center_x - int(size * 0.26), int(center_y - size * 0.06)),
                (center_x - int(size * 0.26), int(center_y - size * 0.28)),
                (center_x - int(size * 0.14), int(center_y - size * 0.16)),
                (center_x,                    int(center_y - size * 0.32)),
                (center_x + int(size * 0.14), int(center_y - size * 0.16)),
                (center_x + int(size * 0.26), int(center_y - size * 0.28)),
                (center_x + int(size * 0.26), int(center_y - size * 0.06)),
            ]
            draw_polygon(crown_points, fill_color, outline_color)
            orb_positions = [
                (-int(size * 0.26), -int(size * 0.28)),
                (0,                 -int(size * 0.32)),
                ( int(size * 0.26), -int(size * 0.28)),
            ]
            for offset_x, offset_y in orb_positions:
                draw_circle(center_x + offset_x, center_y + offset_y, int(size * 0.07), COLOR_ACCENT, outline_color, 1)
 
        elif piece_typ == "K":
            base_width  = int(size * 0.64)
            base_height = int(size * 0.15)
            base_y      = int(center_y + size * 0.30)
            cross_cy    = int(center_y - size * 0.28)
            draw_box(center_x, base_y, base_width, base_height, fill_color, outline_color, corner_radius=4)
            body_points = [
                (center_x - int(size * 0.26), base_y - base_height // 2),
                (center_x + int(size * 0.26), base_y - base_height // 2),
                (center_x + int(size * 0.18), int(center_y - size * 0.04)),
                (center_x - int(size * 0.18), int(center_y - size * 0.04)),
            ]
            draw_polygon(body_points, fill_color, outline_color)
            draw_box(center_x, int(center_y - size * 0.12), int(size * 0.36), int(size * 0.22), fill_color, outline_color, corner_radius=3)
            draw_box(center_x, cross_cy, int(size * 0.12), int(size * 0.40), fill_color, outline_color, corner_radius=2)
            draw_box(center_x, cross_cy - int(size * 0.06), int(size * 0.32), int(size * 0.12), fill_color, outline_color, corner_radius=2)
        return surface
    
class Button:
    def __init__(self, x, y, width, height, text, font=None, is_accent=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font or FONT_SMALL
        self.is_accent = is_accent
        self.hovered = False
 
    def draw(self, surface, selected=False):
        if selected or (self.is_accent and not self.hovered):
            background_color = COLOR_ACCENT
            text_color = COLOR_BACKGROUND
        elif self.hovered:
            background_color = (55, 52, 68)
            text_color = COLOR_TEXT
        else:
            background_color = COLOR_CARD
            text_color = COLOR_TEXT
 
        pygame.draw.rect(surface, background_color, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BORDER, self.rect, 1, border_radius=10)
        draw_text(surface, self.text, self.font, text_color, self.rect.centerx, self.rect.centery)
 
    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
 
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
 
class Renderer:
    def __init__(self, surface):
        self.surface = surface
 
    def draw_board(self, game):
        board = game.board
        for row in range(8):
            for col in range(8):
                square_x = BOARD_OFFSET_X + col * SQUARE_SIZE
                square_y = BOARD_OFFSET_Y + row * SQUARE_SIZE
                square_color = (COLOR_SQUARE_LIGHT if (row + col) % 2 == 0 else COLOR_SQUARE_DARK)
                pygame.draw.rect(self.surface, square_color, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))
 
        if board.last_move:
            for (highlight_row, highlight_col) in board.last_move:
                draw_rounded_rect(self.surface, (255, 210, 50), BOARD_OFFSET_X + highlight_col * SQUARE_SIZE, BOARD_OFFSET_Y + highlight_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, radius=0, alpha=55,)
 
        if game.selected_sq:
            selected_row, selected_col = game.selected_sq
            draw_rounded_rect(
                self.surface, COLOR_SELECTION,
                BOARD_OFFSET_X + selected_col * SQUARE_SIZE,
                BOARD_OFFSET_Y + selected_row * SQUARE_SIZE,
                SQUARE_SIZE, SQUARE_SIZE, radius=0, alpha=130,
            )
            for (move_row, move_col) in game.legal_squares:
                if board.get(move_row, move_col):
                    draw_rounded_rect(
                        self.surface, COLOR_SELECTION,
                        BOARD_OFFSET_X + move_col * SQUARE_SIZE,
                        BOARD_OFFSET_Y + move_row * SQUARE_SIZE,
                        SQUARE_SIZE, SQUARE_SIZE, radius=0, alpha=90,
                    )
                else:
                    dot_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(dot_surface, (100, 200, 80, 110), (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 5)
                    self.surface.blit(dot_surface, (BOARD_OFFSET_X + move_col * SQUARE_SIZE, BOARD_OFFSET_Y + move_row * SQUARE_SIZE))
 
        if (game.board.is_in_check(game.current_turn)and game.status == "playing"):
            king_row, king_col = game.board.find_king(game.current_turn)
            draw_rounded_rect(self.surface, COLOR_CHECK, BOARD_OFFSET_X + king_col * SQUARE_SIZE, BOARD_OFFSET_Y + king_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE, radius=0, alpha=150,)
 
        for row in range(8):
            for col in range(8):
                piece = board.get(row, col)
                if piece:
                    piece_surface = PieceRenderer.get_surface(piece, SQUARE_SIZE)
                    self.surface.blit(piece_surface, (BOARD_OFFSET_X + col * SQUARE_SIZE, BOARD_OFFSET_Y + row * SQUARE_SIZE))
 
        for index in range(8):
            file_color = COLOR_SQUARE_DARK if index % 2 == 0 else COLOR_SQUARE_LIGHT
            file_label = FONT_TINY.render("abcdefgh"[index], True, file_color)
            self.surface.blit(file_label, (BOARD_OFFSET_X + index * SQUARE_SIZE + 3, BOARD_OFFSET_Y + 7 * SQUARE_SIZE + SQUARE_SIZE - 14))
            rank_color = COLOR_SQUARE_LIGHT if index % 2 == 0 else COLOR_SQUARE_DARK
            rank_label = FONT_TINY.render(str(8 - index), True, rank_color)
            self.surface.blit(rank_label, (BOARD_OFFSET_X + 2, BOARD_OFFSET_Y + index * SQUARE_SIZE + 3))
 
        pygame.draw.rect(self.surface, COLOR_BORDER, (BOARD_OFFSET_X - 4, BOARD_OFFSET_Y - 4, SQUARE_SIZE * 8 + 8, SQUARE_SIZE * 8 + 8), 4, border_radius=3,)
 
    def draw_panel(self, game):
        panel_x  = BOARD_OFFSET_X + 8 * SQUARE_SIZE + 28
        panel_width = WINDOW_WIDTH - panel_x - 18
        panel_y  = BOARD_OFFSET_Y
 
        self._draw_timer(game, "b", panel_x, panel_y, panel_width, 96)
        self._draw_timer(game, "w", panel_x, panel_y + SQUARE_SIZE * 8 - 96, panel_width, 96)
 
        clock_mid_y = panel_y + 96 + (SQUARE_SIZE * 8 - 192) // 2
        clock_active = game.waiting_clock and game.status == "playing"
        button_color = COLOR_ACCENT if clock_active else COLOR_CARD
        label_color = COLOR_BACKGROUND if clock_active else COLOR_DIM
 
        draw_rounded_rect(self.surface, button_color, panel_x, clock_mid_y, panel_width, 52, radius=10)
        if clock_active:
            pygame.draw.rect(self.surface, (255, 230, 120), (panel_x, clock_mid_y, panel_width, 52), 2, border_radius=10)
        draw_text(self.surface, "PRESS CLOCK", FONT_SMALL, label_color, panel_x + panel_width // 2, clock_mid_y + 26)
 
        if game.status == "playing":
            side_name   = "White" if game.current_turn == "w" else "Black"
            status_text = "Press clock  →" if game.waiting_clock else f"{side_name} to move"
            draw_text(self.surface, status_text, FONT_TINY, COLOR_DIM, panel_x + panel_width // 2, clock_mid_y + 70)
 
    def _draw_timer(self, game, color, x, y, width, height):
        is_active = (
            game.current_turn == color
            and game.status == "playing"
            and not game.waiting_clock
        )
        is_low          = game.clock.is_low(color)
        background_color = (248, 244, 236) if color == "w" else (32, 29, 40)
        text_color       = COLOR_BACKGROUND if color == "w" else COLOR_TEXT
 
        if is_low and is_active:
            background_color = COLOR_DANGER
            text_color       = (255, 255, 255)
 
        draw_rounded_rect(self.surface, background_color, x, y, width, height, radius=12)
 
        if is_active:
            pygame.draw.rect(self.surface, COLOR_ACCENT, (x, y, width, height), 3, border_radius=12)
 
        player_name = "WHITE" if color == "w" else "BLACK"
        draw_text(self.surface, player_name, FONT_TINY, text_color, x + width // 2, y + 18)
        draw_text(self.surface, game.clock.format(color), FONT_MEDIUM, text_color, x + width // 2, y + height // 2 + 6)
 
    def draw_overlay(self, heading, subtext=""):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((12, 10, 18, 210))
        self.surface.blit(overlay, (0, 0))
        draw_text(self.surface, heading, FONT_LARGE, COLOR_ACCENT, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 44)
        if subtext:
            draw_text(self.surface, subtext, FONT_SMALL, COLOR_DIM, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 16)
        draw_text(self.surface, "Press  R  to return to menu", FONT_TINY, COLOR_DIM, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60)
 
    def draw_promote_menu(self, game):
        promotion_options = ["Q", "R", "B", "N"]
        option_names = {"Q": "Queen", "R": "Rook", "B": "Bishop", "N": "Knight"}
        button_width = 90
        button_height = 100
        gap = 10
        total_width = len(promotion_options) * (button_width + gap) - gap
        start_x = WINDOW_WIDTH // 2 - total_width // 2
        start_y = WINDOW_HEIGHT // 2 - button_height // 2 - 30
 
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 8, 16, 185))
        self.surface.blit(overlay, (0, 0))
 
        draw_rounded_rect(self.surface, COLOR_PANEL, start_x - 24, start_y - 56, total_width + 48, button_height + 120, radius=16,)
        pygame.draw.rect(self.surface, COLOR_BORDER, (start_x - 24, start_y - 56, total_width + 48, button_height + 120), 2, border_radius=16,)
        draw_text(self.surface, "Choose promotion", FONT_SMALL, COLOR_ACCENT, WINDOW_WIDTH // 2, start_y - 28)
 
        clickable_rects = []
        for index, piece_typ in enumerate(promotion_options):
            button_x = start_x + index * (button_width + gap)
            draw_rounded_rect(self.surface, COLOR_CARD, button_x, start_y, button_width, button_height, radius=10)
            pygame.draw.rect(self.surface, COLOR_BORDER, (button_x, start_y, button_width, button_height), 1, border_radius=10)
            piece_surface = PieceRenderer.get_surface(game.current_turn + piece_typ, SQUARE_SIZE)
            offset_x = (button_width - SQUARE_SIZE) // 2
            offset_y = (button_height - SQUARE_SIZE) // 2 - 8
            self.surface.blit(piece_surface, (button_x + offset_x, start_y + offset_y))
            draw_text(self.surface, option_names[piece_typ], FONT_TINY, COLOR_DIM, button_x + button_width // 2, start_y + button_height - 14)
            clickable_rects.append((button_x, start_y, button_width, button_height, piece_typ))
 
        return clickable_rects
 
    def draw_menu(self, selected_minutes, time_options, buttons):
        self.surface.fill(COLOR_BACKGROUND)
        panel_width  = 460
        panel_height = 520
        panel_x = WINDOW_WIDTH // 2 - panel_width // 2
        panel_y = WINDOW_HEIGHT // 2 - panel_height // 2
 
        draw_rounded_rect(self.surface, COLOR_PANEL, panel_x, panel_y, panel_width, panel_height, radius=20)
        pygame.draw.rect(self.surface, COLOR_BORDER, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=20)
 
        draw_text(self.surface, "CHESS", FONT_LARGE,  COLOR_ACCENT, WINDOW_WIDTH // 2, panel_y + 72)
        draw_text(self.surface, "Two Player", FONT_SMALL,  COLOR_DIM,    WINDOW_WIDTH // 2, panel_y + 116)
        pygame.draw.line(self.surface, COLOR_BORDER, (panel_x + 40, panel_y + 148), (panel_x + panel_width - 40, panel_y + 148), 1)
        draw_text(self.surface, "TIME CONTROL", FONT_TINY, COLOR_DIM,    WINDOW_WIDTH // 2, panel_y + 176)
 
        for button, minutes in zip(buttons[:3], time_options):
            button.draw(self.surface, selected=(selected_minutes == minutes))
        buttons[3].draw(self.surface)
 
        pygame.display.flip()