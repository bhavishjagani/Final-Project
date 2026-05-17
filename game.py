import time as time_module
from board import Board, opposite_color
 
class Clock:
    def __init__(self, minutes):
        self.remaining = {"w": minutes * 60.0, "b": minutes * 60.0}
        self.active_color = None
        self._tick_start  = None
 
    def start(self, color):
        self.active_color = color
        self._tick_start  = time_module.time()
 
    def tick(self):
        if self.active_color is None or self._tick_start is None:
            return
        elapsed = time_module.time() - self._tick_start
        self.remaining[self.active_color] = max(0, self.remaining[self.active_color] - elapsed)
        self._tick_start = time_module.time()
 
    def switch(self, color):
        self.tick()
        self.active_color = color
        self._tick_start  = time_module.time()
 
    def stop(self):
        self.tick()
        self.active_color = None
 
    def get_flagged(self):
        for color in ["w", "b"]:
            if self.remaining[color] <= 0:
                return color
        return None
 
    def format(self, color):
        seconds = max(0, int(self.remaining[color]))
        return f"{seconds // 60}:{seconds % 60:02d}"
 
    def is_low(self, color):
        return self.remaining[color] < 20
 
class Game:
    def __init__(self, minutes):
        self.board = Board()
        self.current_turn  = "w"
        self.clock = Clock(minutes)
        self.selected_sq = None
        self.legal_squares = []
        self.status = "playing"
        self.promote_sq = None
        self.waiting_clock = False
 
    def click_square(self, row, col):
        if (self.status != "playing" or self.waiting_clock):
            return
 
        if self.selected_sq:
            if (row, col) in self.legal_squares:
                self._execute_move(self.selected_sq[0], self.selected_sq[1], row, col,)
                return
            self.selected_sq = None
            self.legal_squares = []
 
        piece = self.board.get(row, col)
        if piece and piece[0] == self.current_turn:
            self.selected_sq = (row, col)
            self.legal_squares = self.board.legal_moves(row, col)
 
    def _execute_move(self, from_row, from_col, to_row, to_col):
        needs_promotion = self.board.apply_move(from_row, from_col, to_row, to_col)
        self.selected_sq   = None
        self.legal_squares = []
 
        if needs_promotion:
            self.promote_sq    = (to_row, to_col)
            self.waiting_clock = True
            return
 
        self._finish_move()
 
    def apply_promotion(self, piece_type):
        promote_row, promote_col = self.promote_sq
        self.board.set(promote_row, promote_col, self.current_turn + piece_type)
        self.promote_sq = None
        self._finish_move()
 
    def _finish_move(self):
        opponent = opposite_color(self.current_turn)
 
        if not self.board.has_any_legal_move(opponent):
            if self.board.is_in_check(opponent):
                self.status = "w_win" if self.current_turn == "w" else "b_win"
            else:
                self.status = "draw"
            self.clock.stop()
        elif self.board.is_insufficient_material():
            self.status = "draw"
            self.clock.stop()
        else:
            self.waiting_clock = True
 
    def press_clock(self):
        if (self.status != "playing" or not self.waiting_clock):
            return
        self.waiting_clock = False
        self.current_turn  = opposite_color(self.current_turn)
        self.clock.switch(self.current_turn)
 
    def tick(self):
        if (self.status != "playing" or self.waiting_clock):
            return
        self.clock.tick()
        flagged = self.clock.get_flagged()
        if flagged:
            self.status = "b_win" if flagged == "w" else "w_win"
            self.clock.stop()