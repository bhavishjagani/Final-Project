import pygame, sys, time, math
pygame.init()
pygame.font.init()
 
W, H = 1000, 830
SQ = 72
BOARD_X = 140
BOARD_Y = (H - SQ * 8) // 2
 
C = {"bg":       (15, 15, 20), "panel":    (22, 22, 30), "light":    (240, 217, 181), "dark":     (181, 136, 99), "sel":      (106, 168, 79, 180), "move":     (106, 168, 79, 120),
    "check":    (220, 50, 50, 200), "border":   (60, 60, 80),  "text":     (220, 220, 230), "dim":      (120, 120, 140), "accent":   (255, 200, 80),  "white_sq": (240, 217, 181),
    "black_sq": (181, 136, 99), "w_timer":  (245, 245, 245), "b_timer":  (30, 30, 40), "danger":   (200, 60, 60), "btn":      (40, 40, 55), "btn_h":    (60, 60, 80), "overlay":  (10, 10, 15, 210),}
 
font_name = "SF Pro Display" if "SF Pro Display" in pygame.font.get_fonts() else "helvetica"
FONT_L = pygame.font.SysFont(font_name, 42, bold=True)
FONT_M = pygame.font.SysFont(font_name, 28, bold=True)
FONT_S = pygame.font.SysFont(font_name, 18)
FONT_XS = pygame.font.SysFont(font_name, 14)
 
INIT_BOARD = [
    ["bR","bN","bB","bQ","bK","bB","bN","bR"],
    ["bP","bP","bP","bP","bP","bP","bP","bP"],
    [None]*8, [None]*8, [None]*8, [None]*8,
    ["wP","wP","wP","wP","wP","wP","wP","wP"],
    ["wR","wN","wB","wQ","wK","wB","wN","wR"],
]
 
def copy_board(b): 
    return [row[:] for row in b]
def color_of(p): 
    return p[0] if p else None
def type_of(p): 
    return p[1:] if p else None
def in_bounds(r, c): 
    return 0 <= r < 8 and 0 <= c < 8

def find_king(board, col):
    for r in range(8):
        for c in range(8):
            if board[r][c] == col + "K": return (r, c)
    return None

def is_attacked(board, r, c, by_col):
    for fr in range(8):
        for fc in range(8):
            p = board[fr][fc]
            if p and p[0] == by_col:
                if (r, c) in raw_moves(board, fr, fc, None): return True
    return False

def raw_moves(board, r, c, ep):
    p = board[r][c]
    if not p: return []
    col, typ, opp = p[0], p[1:], 'b' if p[0] == 'w' else 'w'
    moves = []

    def slide(dirs):
        for dr, dc in dirs:
            nr, nc = r+dr, c+dc
            while in_bounds(nr, nc):
                t = board[nr][nc]
                if t:
                    if t[0] == opp: moves.append((nr, nc))
                    break
                moves.append((nr, nc))
                nr += dr; nc += dc

    if typ == "P":
        d = -1 if col == "w" else 1
        start = 6 if col == "w" else 1
        if in_bounds(r+d, c) and not board[r+d][c]:
            moves.append((r+d, c))
            if r == start and not board[r+2*d][c]: moves.append((r+2*d, c))
        for dc in [-1, 1]:
            nr, nc = r+d, c+dc
            if in_bounds(nr, nc):
                if (board[nr][nc] and board[nr][nc][0] == opp) or (ep and (nr, nc) == ep):
                    moves.append((nr, nc))
    elif typ == "N":
        for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr, nc) and (not board[nr][nc] or board[nr][nc][0] == opp):
                moves.append((nr, nc))
    elif typ in ["B", "R", "Q"]:
        dirs = []
        if typ != "R": dirs.extend([(-1,-1),(-1,1),(1,-1),(1,1)])
        if typ != "B": dirs.extend([(-1,0),(1,0),(0,-1),(0,1)])
        slide(dirs)
    elif typ == "K":
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr==0 and dc==0: continue
                nr, nc = r+dr, c+dc
                if in_bounds(nr, nc) and (not board[nr][nc] or board[nr][nc][0] == opp):
                    moves.append((nr, nc))
    return moves

def legal_moves(board, r, c, ep, castling):
    p = board[r][c]
    if not p: return []
    col, opp, typ = p[0], 'b' if p[0] == 'w' else 'w', p[1:]
    result = []
    
    for (nr, nc) in raw_moves(board, r, c, ep):
        nb = copy_board(board)
        if ep and typ == "P" and (nr, nc) == ep:
            nb[r][nc] = None 
        
        nb[nr][nc] = p
        nb[r][c] = None
        
        if not is_attacked(nb, *find_king(nb, col), opp):
            result.append((nr, nc))
            
    if typ == "K" and not is_attacked(board, r, c, opp):
        row = 7 if col == "w" else 0
        if r == row and c == 4:
            for side in ["K", "Q"]:
                if castling.get(col+side):
                    pass 
    return result

def all_legal_moves(board, col, ep, castling):
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p and p[0] == col and legal_moves(board, r, c, ep, castling):
                return True
    return False
 
def is_check(board, col):
    opp = "b" if col == "w" else "w"
    kr, kc = find_king(board, col)
    return is_attacked(board, kr, kc, opp)
 
def is_insufficient(board):
    pieces = []
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p:
                pieces.append(p)
    types = [type_of(p) for p in pieces]
    if len(pieces) == 2:
        return True
    if len(pieces) == 3 and ("N" in types or "B" in types):
        return True
    return False
 
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()
 
def draw_text(surf, text, font, color, cx, cy, anchor="center"):
    s = font.render(text, True, color)
    r = s.get_rect()
    if anchor == "center":
        r.center = (cx, cy)
    elif anchor == "right":
        r.midright = (cx, cy)
    elif anchor == "left":
        r.midleft = (cx, cy)
    surf.blit(s, r)
 
def draw_rounded_rect(surf, color, rect, radius=8, alpha=None):
    if alpha is not None:
        s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
        pygame.draw.rect(s, (*color[:3], alpha), (0,0,rect[2],rect[3]), border_radius=radius)
        surf.blit(s, (rect[0], rect[1]))
    else:
        pygame.draw.rect(surf, color, rect, border_radius=radius)
 
def draw_piece(surf, p, x, y, small=False):
    col = color_of(p)
    typ = type_of(p)
    s = int(SQ * 0.7) if not small else int(SQ * 0.5)
    cx = x + SQ // 2
    cy = y + SQ // 2
    wc = (240, 235, 220)
    bc = (40, 35, 30)
    fc = wc if col == "w" else bc
    oc = (60, 50, 40) if col == "w" else (200, 190, 170)
 
    def circle(sx, sy, r, fill=None, out=None, w=0):
        if fill:
            pygame.draw.circle(surf, fill, (sx, sy), r)
        if out:
            pygame.draw.circle(surf, out, (sx, sy), r, w or 2)
 
    def rect(rx, ry, rw, rh, fill=None, out=None, rad=3):
        rct = pygame.Rect(rx - rw//2, ry - rh//2, rw, rh)
        if fill:
            pygame.draw.rect(surf, fill, rct, border_radius=rad)
        if out:
            pygame.draw.rect(surf, out, rct, 2, border_radius=rad)
 
    def poly(pts, fill, out=None):
        pygame.draw.polygon(surf, fill, pts)
        if out:
            pygame.draw.polygon(surf, out, pts, 2)
 
    sh = (0, 0, 0)
 
    if typ == "P":
        pygame.draw.ellipse(surf, sh, (cx-s//3, cy+s//4, s//1.5, s//5))
        rect(cx, cy + s//8, s//2, s//3, fc, oc)
        circle(cx, cy - s//6, s//3, fc, oc)
 
    elif typ == "R":
        pygame.draw.ellipse(surf, sh, (cx-s//2+2, cy+s//2-4, s, s//5))
        rect(cx, cy + s//5, int(s*0.7), int(s*0.35), fc, oc)
        rect(cx, cy - s//8, int(s*0.55), int(s*0.55), fc, oc)
        for dx in [-s//4, 0, s//4]:
            rect(cx+dx, cy - s//2 + s//8, s//5, s//4, fc, oc)
 
    elif typ == "N":
        pygame.draw.ellipse(surf, sh, (cx-s//2+2, cy+s//2-4, s, s//5))
        pts_body = [
            (cx - s//4, cy + s//2 - s//8),
            (cx + s//3, cy + s//2 - s//8),
            (cx + s//3, cy),
            (cx + s//2, cy - s//3),
            (cx + s//4, cy - s//2),
            (cx - s//8, cy - s//3),
            (cx - s//3, cy - s//4),
            (cx - s//4, cy + s//8),
        ]
        poly(pts_body, fc, oc)
        circle(cx + s//5, cy - s//3, s//8, oc)
 
    elif typ == "B":
        pygame.draw.ellipse(surf, sh, (cx-s//2+2, cy+s//2-4, s, s//5))
        rect(cx, cy + s//3, int(s*0.65), s//5, fc, oc)
        pts = [
            (cx, cy - s//2),
            (cx - s//3, cy + s//5),
            (cx + s//3, cy + s//5),
        ]
        poly(pts, fc, oc)
        circle(cx, cy - s//2 + s//10, s//8, oc)
        circle(cx, cy + s//16, s//5, fc, oc)
 
    elif typ == "Q":
        pygame.draw.ellipse(surf, sh, (cx-s//2+2, cy+s//2-4, s, s//5))
        rect(cx, cy + s//3, int(s*0.7), s//5, fc, oc)
        rect(cx, cy + s//8, int(s*0.55), int(s*0.45), fc, oc)
        for i, dx in enumerate([-s//3, -s//6, 0, s//6, s//3]):
            h = s//4 if i % 2 == 0 else s//3
            circle(cx + dx, cy - s//4 - h//2, s//8, fc, oc, 2)
        pygame.draw.arc(surf, oc, (cx-s//3, cy-s//3, int(s*0.65), int(s*0.55)), 0, 3.14, 2)
 
    elif typ == "K":
        pygame.draw.ellipse(surf, sh, (cx-s//2+2, cy+s//2-4, s, s//5))
        rect(cx, cy + s//3, int(s*0.7), s//5, fc, oc)
        rect(cx, cy + s//10, int(s*0.5), int(s*0.5), fc, oc)
        rect(cx, cy - s//3, s//5, int(s*0.55), fc, oc)
        rect(cx, cy - s//3, int(s*0.45), s//5, fc, oc)
 
def format_time(secs):
    secs = max(0, int(secs))
    m = secs // 60
    s = secs % 60
    return f"{m}:{s:02d}"
 
class Button:
    def __init__(self, x, y, w, h, text, font=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font or FONT_S
        self.hovered = False
 
    def draw(self, surf, selected=False):
        col = C["accent"] if selected else (C["btn_h"] if self.hovered else C["btn"])
        tcol = C["bg"] if selected else C["text"]
        draw_rounded_rect(surf, col, self.rect, radius=10)
        draw_text(surf, self.text, self.font, tcol, self.rect.centerx, self.rect.centery)
 
    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)
 
    def clicked(self, pos):
        return self.rect.collidepoint(pos)
 
class Game:
    def __init__(self, minutes):
        self.board = copy_board(INIT_BOARD)
        self.turn = "w"
        self.selected = None
        self.moves = []
        self.ep = None
        self.castling = {"wK":True,"wQ":True,"bK":True,"bQ":True}
        self.time = {
            "w": minutes * 60.0,
            "b": minutes * 60.0,
        }
        self.active_start = time.time()
        self.status = "playing"
        self.promote_pawn = None
        self.move_log = []
        self.last_move = None
        self.clock_pressed = False
        self.waiting_clock = False
 
    def tick(self):
        if self.status != "playing" or self.waiting_clock:
            return
        elapsed = time.time() - self.active_start
        self.time[self.turn] -= elapsed
        self.active_start = time.time()
        if self.time[self.turn] <= 0:
            self.time[self.turn] = 0
            self.status = "w_win" if self.turn == "b" else "b_win"
 
    def click_square(self, r, c):
        if self.status != "playing" or self.waiting_clock:
            return
        p = self.board[r][c]
        if self.selected:
            sr, sc = self.selected
            if (r, c) in self.moves:
                self.do_move(sr, sc, r, c)
                return
            self.selected = None
            self.moves = []
        if p and color_of(p) == self.turn:
            self.selected = (r, c)
            self.moves = legal_moves(self.board, r, c, self.ep, self.castling)
 
    def do_move(self, fr, fc, tr, tc):
        p = self.board[fr][fc]
        col = color_of(p)
        typ = type_of(p)
        cap = self.board[tr][tc]
 
        if typ == "P" and self.ep and (tr, tc) == self.ep:
            self.board[fr][tc] = None
            cap = col
 
        self.board[tr][tc] = p
        self.board[fr][fc] = None
        self.last_move = ((fr, fc), (tr, tc))
 
        if typ == "K":
            if abs(tc - fc) == 2:
                row = fr
                if tc == 6:
                    self.board[row][5] = col+"R"
                    self.board[row][7] = None
                else:
                    self.board[row][3] = col+"R"
                    self.board[row][0] = None
            self.castling[col+"K"] = False
            self.castling[col+"Q"] = False
 
        if typ == "R":
            if fc == 0: self.castling[col+"Q"] = False
            if fc == 7: self.castling[col+"K"] = False
 
        self.ep = None
        if typ == "P" and abs(tr - fr) == 2:
            self.ep = ((fr + tr) // 2, fc)
 
        if typ == "P" and (tr == 0 or tr == 7):
            self.promote_pawn = (tr, tc)
            self.waiting_clock = True
            self.selected = None
            self.moves = []
            return
 
        self.finish_move()
 
    def promote(self, piece_type):
        if self.promote_pawn:
            r, c = self.promote_pawn
            self.board[r][c] = self.turn + piece_type
            self.promote_pawn = None
        self.waiting_clock = True
        self.finish_move_after_promote()
 
    def finish_move_after_promote(self):
        self.finish_move()
 
    def finish_move(self):
        opp = "b" if self.turn == "w" else "w"
        if not all_legal_moves(self.board, opp, self.ep, self.castling):
            if is_check(self.board, opp):
                self.status = "w_win" if self.turn == "w" else "b_win"
            else:
                self.status = "draw"
        elif is_insufficient(self.board):
            self.status = "draw"
        self.selected = None
        self.moves = []
        self.waiting_clock = True
        self.active_start = time.time()
 
    def press_clock(self):
        if self.status != "playing":
            return
        if self.waiting_clock:
            self.waiting_clock = False
            self.turn = "b" if self.turn == "w" else "w"
            self.active_start = time.time()
 
def draw_board(surf, game):
    for r in range(8):
        for c in range(8):
            x = BOARD_X + c * SQ
            y = BOARD_Y + r * SQ
            is_light = (r + c) % 2 == 0
            base = C["light"] if is_light else C["dark"]
            pygame.draw.rect(surf, base, (x, y, SQ, SQ))
 
    if game.last_move:
        for (lr, lc) in game.last_move:
            x = BOARD_X + lc * SQ
            y = BOARD_Y + lr * SQ
            s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
            pygame.draw.rect(s, (255, 215, 0, 60), (0, 0, SQ, SQ))
            surf.blit(s, (x, y)) 
 
    if game.selected:
        sr, sc = game.selected
        x = BOARD_X + sc * SQ
        y = BOARD_Y + sr * SQ
        s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        pygame.draw.rect(s, (*C["sel"][:3], 160), (0, 0, SQ, SQ))
        surf.blit(s, (x, y))
 
        for (mr, mc) in game.moves:
            mx = BOARD_X + mc * SQ
            my = BOARD_Y + mr * SQ
            ms = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
            if game.board[mr][mc]:
                pygame.draw.rect(ms, (*C["sel"][:3], 100), (0, 0, SQ, SQ))
            else:
                pygame.draw.circle(ms, (*C["move"][:3], 130), (SQ//2, SQ//2), SQ//5)
            surf.blit(ms, (mx, my))
 
    if is_check(game.board, game.turn) and game.status == "playing":
        kr, kc = find_king(game.board, game.turn)
        x = BOARD_X + kc * SQ
        y = BOARD_Y + kr * SQ
        s = pygame.Surface((SQ, SQ), pygame.SRCALPHA)
        pygame.draw.rect(s, (*C["check"][:3], 160), (0, 0, SQ, SQ))
        surf.blit(s, (x, y))
 
    for r in range(8):
        for c in range(8):
            p = game.board[r][c]
            if p:
                draw_piece(surf, p, BOARD_X + c*SQ, BOARD_Y + r*SQ)
 
    for i in range(8):
        label_c = C["dark"] if i % 2 == 0 else C["light"]
        lx = BOARD_X + i * SQ + 3
        ly = BOARD_Y + 7 * SQ + SQ - 14
        s = FONT_XS.render("abcdefgh"[i], True, label_c)
        surf.blit(s, (lx, ly))
        nr = FONT_XS.render(str(8 - i), True, label_c if i%2==0 else C["dark"])
        s2 = FONT_XS.render(str(8-i), True, C["dark"] if i%2==0 else C["light"])
        surf.blit(s2, (BOARD_X + 2, BOARD_Y + i*SQ + 3))
 
def draw_timer_panel(surf, game, col, x, y, w, h):
    is_active = (game.turn == col and game.status == "playing" and not game.waiting_clock)
    secs = game.time[col]
    low = secs < 30
    bg = C["w_timer"] if col == "w" else C["b_timer"]
    tc = C["bg"] if col == "w" else C["text"]
    if low and is_active:
        bg = C["danger"]
        tc = (255, 255, 255)
    draw_rounded_rect(surf, bg, (x, y, w, h), radius=12)
    if is_active:
        pygame.draw.rect(surf, C["accent"], (x, y, w, h), width=3, border_radius=12)
    name = "WHITE" if col == "w" else "BLACK"
    draw_text(surf, name, FONT_XS, tc if not low or not is_active else (255,255,255), x + w//2, y + 18)
    draw_text(surf, format_time(secs), FONT_M, tc, x + w//2, y + h//2 + 4)
 
def draw_clock_button(surf, game, x, y, w, h):
    can = game.waiting_clock and game.status == "playing"
    col = C["accent"] if can else C["btn"]
    tc = C["bg"] if can else C["dim"]
    draw_rounded_rect(surf, col, (x, y, w, h), radius=10)
    draw_text(surf, "PRESS CLOCK", FONT_XS, tc, x+w//2, y+h//2)
 
def draw_panel(surf, game):
    px = BOARD_X + 8*SQ + 24
    pw = W - px - 16
    py = BOARD_Y
 
    draw_timer_panel(surf, game, "b", px, py, pw, 90)
    draw_timer_panel(surf, game, "w", px, py + 90 + 8*SQ - 90, pw, 90)
 
    mid_y = py + 90 + (8*SQ - 180) // 2 - 24
    draw_clock_button(surf, game, px, mid_y, pw, 48)
 
    turn_y = mid_y + 64
    turn_col = "White" if game.turn == "w" else "Black"
    label = f"{turn_col}'s turn" if game.status == "playing" else ""
    if game.waiting_clock:
        label = "Press clock →"
    draw_text(surf, label, FONT_XS, C["dim"], px + pw//2, turn_y)
 
def draw_overlay(surf, text, sub=""):
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    s.fill((10, 10, 15, 200))
    surf.blit(s, (0, 0))
    draw_text(surf, text, FONT_L, C["accent"], W//2, H//2 - 40)
    if sub:
        draw_text(surf, sub, FONT_S, C["dim"], W//2, H//2 + 20)
    draw_text(surf, "Press R to restart", FONT_XS, C["dim"], W//2, H//2 + 70)
 
def draw_promote_menu(surf, game):
    col = game.turn
    opts = ["Q","R","B","N"]
    bw, bh = 80, 80
    total = len(opts) * bw + (len(opts)-1)*8
    sx = W//2 - total//2
    sy = H//2 - bh//2 - 20
 
    s = pygame.Surface((W, H), pygame.SRCALPHA)
    s.fill((10,10,15,180))
    surf.blit(s, (0,0))
 
    draw_rounded_rect(surf, C["panel"], (sx-20, sy-50, total+40, bh+100), radius=14)
    draw_text(surf, "Promote pawn", FONT_S, C["accent"], W//2, sy - 24)
 
    for i, typ in enumerate(opts):
        bx = sx + i*(bw+8)
        draw_rounded_rect(surf, C["btn_h"], (bx, sy, bw, bh), radius=10)
        draw_piece(surf, col+typ, bx, sy)
 
    return [(sx + i*(bw+8), sy, bw, bh, opts[i]) for i in range(len(opts))]
 
def draw_menu(selected_time, time_opts, buttons):
    screen.fill(C["bg"])
    draw_rounded_rect(screen, C["panel"], (W//2-220, 80, 440, H-160), radius=18)
    draw_text(screen, "CHESS", FONT_L, C["accent"], W//2, 160)
    draw_text(screen, "Two Player", FONT_S, C["dim"], W//2, 210)
 
    draw_text(screen, "Select Time Control", FONT_XS, C["dim"], W//2, 290)
    for i, (b, mins) in enumerate(zip(buttons[:3], time_opts)):
        b.draw(screen, selected=selected_time == mins)
 
    buttons[3].draw(screen)
    pygame.display.flip()
 
def main():
    time_opts = [1, 3, 5]
    selected_time = 3
    btn_y = 320
    time_btns = [Button(W//2-150+i*100, btn_y, 86, 44, f"{t} min") for i, t in enumerate(time_opts)]
    start_btn = Button(W//2-100, 420, 200, 52, "START GAME", FONT_M)
    all_btns = time_btns + [start_btn]
 
    state = "menu"
    game = None
 
    while True:
        mx, my = pygame.mouse.get_pos()
        for b in all_btns:
            b.update((mx, my))
 
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
 
            if state == "menu":
                if e.type == pygame.MOUSEBUTTONDOWN:
                    for b, t in zip(time_btns, time_opts):
                        if b.clicked((mx, my)):
                            selected_time = t
                    if start_btn.clicked((mx, my)):
                        game = Game(selected_time)
                        state = "game"
 
            elif state == "game":
                if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    state = "menu"
                    game = None
 
                if e.type == pygame.MOUSEBUTTONDOWN:
                    gx, gy = mx - BOARD_X, my - BOARD_Y
                    c2, r2 = gx // SQ, gy // SQ
 
                    if game.promote_pawn:
                        rects = draw_promote_menu(screen, game)
                        for (bx, by, bw, bh, typ) in rects:
                            if bx <= mx <= bx+bw and by <= my <= by+bh:
                                game.promote(typ)
                        continue
 
                    px2 = BOARD_X + 8*SQ + 24
                    pw2 = W - px2 - 16
                    clock_y = BOARD_Y + 90 + (8*SQ - 180)//2 - 24
                    clock_rect = pygame.Rect(px2, clock_y, pw2, 48)
                    if clock_rect.collidepoint(mx, my):
                        game.press_clock()
                    elif 0 <= r2 < 8 and 0 <= c2 < 8:
                        game.click_square(r2, c2)
 
        if state == "menu":
            draw_menu(selected_time, time_opts, all_btns)
 
        elif state == "game" and game:
            game.tick()
            screen.fill(C["bg"])
 
            bx2 = BOARD_X
            by2 = BOARD_Y
            bord_r = pygame.Rect(bx2-6, by2-6, 8*SQ+12, 8*SQ+12)
            draw_rounded_rect(screen, C["border"], bord_r, radius=4)
 
            draw_board(screen, game)
            draw_panel(screen, game)
 
            if game.promote_pawn:
                draw_promote_menu(screen, game)
            elif game.status == "w_win":
                draw_overlay(screen, "White Wins!", "Checkmate" if not game.time["b"] > 0 else "On time")
            elif game.status == "b_win":
                draw_overlay(screen, "Black Wins!", "Checkmate" if not game.time["w"] > 0 else "On time")
            elif game.status == "draw":
                draw_overlay(screen, "Draw", "Stalemate or insufficient material")
 
            pygame.display.flip()
 
        clock.tick(60)
 
main()