from piece import Pawn, Piece, King, Knight, Rook, Bishop, Queen


class Game:
    def __init__(self) -> None:
        self.board = {f'{x}{y}': None for x in Piece.x_line for y in range(1, 9)}
        self.generate_board()

    def generate_board(self):
        pieces = [(Pawn, 2, 7, '♟', '♙'), (King, 1, 8, '♚', '♔'), (Knight, 1, 8, '♞', '♘'),
                  (Rook, 1, 8, '♜', '♖'), (Bishop, 1, 8, '♝', '♗'), (Queen, 1, 8, '♛', '♕')]
        for piece, white_y, black_y, white_icon, black_icon in pieces:
            if piece == Pawn:
                for i in range(1, 9):
                    self.board.update(piece('w', i, white_y, white_icon).get())
                    self.board.update(piece('b', i, black_y, black_icon).get())
            else:
                if piece in [King, Queen]:
                    self.board.update(piece('w', 5 if piece == King else 4, white_y, white_icon).get())
                    self.board.update(piece('b', 5 if piece == King else 4, black_y, black_icon).get())
                else:
                    for i in [2, 7] if piece == Knight else [1, 8]:
                        self.board.update(piece('w', i, white_y, white_icon).get())
                        self.board.update(piece('b', i, black_y, black_icon).get())

    def get_board_string(self):
        l = list(self.board.values())
        l = ['_' if not i else i for i in l]
        l = [l[i : i + 8] for i in range(0, 64, 8)]
        board_string = ""
        for i, row in enumerate(l):
            board_string += " | ".join(str(square) for square in row) + "\n"
        return board_string


    def get_board(self):
        l = list(self.board.values())
        l = ['_' if not i else i for i in l]
        l = [l[i : i + 8] for i in range(0, 64, 8)]
        for i, row in enumerate(l):
            print(" | ".join(str(square) for square in row))


    def make_move(self, from_, to_):
        piece = self.board[from_]
        if self.validate_move(from_, to_):
            piece.pos = to_
            piece.x, piece.y = piece.get_x_y()
            self.board[to_] = piece
            self.board[from_] = None
            if isinstance(piece, Pawn):
                piece.first_move = False
            return True
        else:
            self.board[from_] = piece
            return False
    def validate_move(self, from_, to_):
        piece = self.board[from_]
        enemy = self.board[to_]
        if not piece:
            return False
        moves = piece.available_moves()

        if isinstance(piece, (Rook, Pawn, Bishop, Queen)):
            barriers = self.check_barriers(from_, to_, moves)
        else:
            barriers = True

        return (
            barriers
            and to_ in moves
            and isinstance(piece, Piece)
            and (enemy is None or piece.color != enemy.color)
        )

    def check_barriers(self, from_, to_, moves):
        m = []
        for move in moves:
            if (from_[0] > to_[0] or from_[1] > to_[1]) and isinstance(
                self.board[move], Piece
            ):
                if (from_[0] > move[0] > to_[0]) or (from_[1] > move[1] > to_[1]):
                    m.append(move)
            elif (from_[0] < to_[0] or from_[1] < to_[1]) and isinstance(
                self.board[move], Piece
            ):
                if (from_[0] < move[0] < to_[0]) or (from_[1] < move[1] < to_[1]):
                    m.append(move)
        return m == []


