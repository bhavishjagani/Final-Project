from constants import INITIAL_BOARD 
 
def copy_board(board):
    return [row[:] for row in board]
 
def piece_color(piece):
    return piece[0] if piece else None
 
def piece_type(piece):
    return piece[1:] if piece else None
 
def opposite_color(color):
    return "b" if color == "w" else "w"
 
def in_bounds(row, col):
    return 0 <= row < 8 and 0 <= col < 8
 
class Board:
    def __init__(self):
        self.squares = copy_board(INITIAL_BOARD)
        self.en_passant = None
        self.castling = {"wK": True, "wQ": True, "bK": True, "bQ": True}
        self.last_move = None
 
    def get(self, row, col):
        return self.squares[row][col]
 
    def set(self, row, col, piece):
        self.squares[row][col] = piece
 
    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                if self.squares[row][col] == color + "K":
                    return (row, col)
        return (0, 0)
 
    def is_square_attacked(self, row, col, by_color):
        for from_row in range(8):
            for from_col in range(8):
                piece = self.squares[from_row][from_col]
                if (
                    piece
                    and piece[0] == by_color
                    and (row, col) in self._raw_moves(from_row, from_col, None)
                ):
                    return True
        return False
 
    def _raw_moves(self, row, col, en_passant_square):
        piece = self.squares[row][col]
        if not piece:
            return []
 
        piece_col  = piece[0]
        piece_typ  = piece[1:]
        enemy_col  = opposite_color(piece_col)
        moves      = []
 
        def slide(directions):
            for delta_row, delta_col in directions:
                next_row = row + delta_row
                next_col = col + delta_col
                while in_bounds(next_row, next_col):
                    target = self.squares[next_row][next_col]
                    if target:
                        if target[0] == enemy_col:
                            moves.append((next_row, next_col))
                        break
                    moves.append((next_row, next_col))
                    next_row += delta_row
                    next_col += delta_col
 
        if piece_typ == "P":
            direction = -1 if piece_col == "w" else 1
            start_row = 6 if piece_col == "w" else 1
            if (in_bounds(row + direction, col) and not self.squares[row + direction][col]):
                moves.append((row + direction, col))
                if (row == start_row and not self.squares[row + 2 * direction][col]):
                    moves.append((row + 2 * direction, col))
            for col_delta in [-1, 1]:
                target_row = row + direction
                target_col = col + col_delta
                if in_bounds(target_row, target_col):
                    target = self.squares[target_row][target_col]
                    if ((target and target[0] == enemy_col)or (en_passant_square and (target_row, target_col) == en_passant_square)):
                        moves.append((target_row, target_col))
 
        elif piece_typ == "N":
            for delta_row, delta_col in [
                (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                (1, -2),  (1, 2),  (2, -1),  (2, 1),
            ]:
                next_row = row + delta_row
                next_col = col + delta_col
                if in_bounds(next_row, next_col):
                    target = self.squares[next_row][next_col]
                    if not target or target[0] == enemy_col:
                        moves.append((next_row, next_col))
 
        elif piece_typ in ["B", "R", "Q"]:
            directions = []
            if piece_typ != "R":
                directions.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
            if piece_typ != "B":
                directions.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])
            slide(directions)
 
        elif piece_typ == "K":
            for delta_row in [-1, 0, 1]:
                for delta_col in [-1, 0, 1]:
                    if delta_row == 0 and delta_col == 0:
                        continue
                    next_row = row + delta_row
                    next_col = col + delta_col
                    if in_bounds(next_row, next_col):
                        target = self.squares[next_row][next_col]
                        if not target or target[0] == enemy_col:
                            moves.append((next_row, next_col))
 
        return moves
 
    def legal_moves(self, row, col):
        piece = self.squares[row][col]
        if not piece:
            return []
 
        piece_col  = piece[0]
        piece_typ  = piece[1:]
        enemy_col  = opposite_color(piece_col)
        legal      = []
 
        for (target_row, target_col) in self._raw_moves(row, col, self.en_passant):
            new_squares = copy_board(self.squares)
            if (
                self.en_passant
                and piece_typ == "P"
                and (target_row, target_col) == self.en_passant
            ):
                new_squares[row][target_col] = None
            new_squares[target_row][target_col] = piece
            new_squares[row][col] = None
 
            temp_board           = Board.__new__(Board)
            temp_board.squares   = new_squares
            temp_board.en_passant = None
            temp_board.castling  = self.castling
            temp_board.last_move = None
 
            king_row, king_col = temp_board.find_king(piece_col)
            if not temp_board.is_square_attacked(king_row, king_col, enemy_col):
                legal.append((target_row, target_col))
 
        if (
            piece_typ == "K"
            and not self.is_square_attacked(row, col, enemy_col)
        ):
            castle_row = 7 if piece_col == "w" else 0
            if row == castle_row and col == 4:
                if (
                    self.castling.get(piece_col + "K")
                    and not self.squares[castle_row][5]
                    and not self.squares[castle_row][6]
                    and not self.is_square_attacked(castle_row, 5, enemy_col)
                    and not self.is_square_attacked(castle_row, 6, enemy_col)
                ):
                    new_squares = copy_board(self.squares)
                    new_squares[castle_row][6] = piece_col + "K"
                    new_squares[castle_row][4] = None
                    temp_board           = Board.__new__(Board)
                    temp_board.squares   = new_squares
                    temp_board.en_passant = None
                    temp_board.castling  = self.castling
                    temp_board.last_move = None
                    king_row, king_col   = temp_board.find_king(piece_col)
                    if not temp_board.is_square_attacked(king_row, king_col, enemy_col):
                        legal.append((castle_row, 6))
 
                if (
                    self.castling.get(piece_col + "Q")
                    and not self.squares[castle_row][3]
                    and not self.squares[castle_row][2]
                    and not self.squares[castle_row][1]
                    and not self.is_square_attacked(castle_row, 3, enemy_col)
                    and not self.is_square_attacked(castle_row, 2, enemy_col)
                ):
                    new_squares = copy_board(self.squares)
                    new_squares[castle_row][2] = piece_col + "K"
                    new_squares[castle_row][4] = None
                    temp_board = Board.__new__(Board)
                    temp_board.squares = new_squares
                    temp_board.en_passant = None
                    temp_board.castling = self.castling
                    temp_board.last_move= None
                    king_row, king_col  = temp_board.find_king(piece_col)
                    if not temp_board.is_square_attacked(king_row, king_col, enemy_col):
                        legal.append((castle_row, 2))
        return legal
 
    def has_any_legal_move(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if (
                    piece
                    and piece[0] == color
                    and self.legal_moves(row, col)
                ):
                    return True
        return False
 
    def is_in_check(self, color):
        king_row, king_col = self.find_king(color)
        return self.is_square_attacked(king_row, king_col, opposite_color(color))
 
    def apply_move(self, from_row, from_col, to_row, to_col):
        piece     = self.squares[from_row][from_col]
        piece_col = piece[0]
        piece_typ = piece[1:]
 
        if (
            piece_typ == "P"
            and self.en_passant
            and (to_row, to_col) == self.en_passant
        ):
            self.squares[from_row][to_col] = None
 
        self.squares[to_row][to_col]     = piece
        self.squares[from_row][from_col] = None
        self.last_move = ((from_row, from_col), (to_row, to_col))
        self.en_passant = None
 
        if piece_typ == "K":
            if abs(to_col - from_col) == 2:
                if to_col == 6:
                    self.squares[from_row][5] = piece_col + "R"
                    self.squares[from_row][7] = None
                else:
                    self.squares[from_row][3] = piece_col + "R"
                    self.squares[from_row][0] = None
            self.castling[piece_col + "K"] = False
            self.castling[piece_col + "Q"] = False
 
        if piece_typ == "R":
            if from_col == 0:
                self.castling[piece_col + "Q"] = False
            if from_col == 7:
                self.castling[piece_col + "K"] = False
 
        if piece_typ == "P" and abs(to_row - from_row) == 2:
            self.en_passant = ((from_row + to_row) // 2, from_col)
 
        return piece_typ == "P" and (to_row == 0 or to_row == 7)
 
    def is_insufficient_material(self):
        all_pieces = [
            self.squares[row][col]
            for row in range(8)
            for col in range(8)
            if self.squares[row][col]
        ]
        piece_types = [piece[1:] for piece in all_pieces]
        if len(all_pieces) == 2:
            return True
        if len(all_pieces) == 3 and ("N" in piece_types or "B" in piece_types):
            return True
        return False