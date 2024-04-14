from piece import Pawn, King, Knight, Rook, Bishop, Queen, Piece


class ChessBoard:
    def __init__(self):
        self.board = {(x,y): None for x in 'abcdefgh' for y in range(1, 9)}
        self.place_pieces()
        self.x_line = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def place_pieces(self):
        """
        Place initial pieces on the board.
        """
        # White pieces
        self.update_board(Rook('w', 1, 1, '♖'))
        self.update_board(Knight('w', 2, 1, '♘'))
        self.update_board(Bishop('w', 3, 1, '♗'))
        self.update_board(Queen('w', 4, 1, '♕'))
        self.update_board(King('w', 5, 1, '♔'))
        self.update_board(Bishop('w', 6, 1, '♗'))
        self.update_board(Knight('w', 7, 1, '♘'))
        self.update_board(Rook('w', 8, 1, '♖'))
        for i in range(1, 9):
            self.update_board(Pawn('w', i, 2, '♙'))

        self.update_board(Rook('b', 1, 8, '♜'))
        self.update_board(Knight('b', 2, 8, '♞'))
        self.update_board(Bishop('b', 3, 8, '♝'))
        self.update_board(Queen('b', 4, 8, '♛'))
        self.update_board(King('b', 5, 8, '♚'))
        self.update_board(Bishop('b', 6, 8, '♝'))
        self.update_board(Knight('b', 7, 8, '♞'))
        self.update_board(Rook('b', 8, 8, '♜'))
        for i in range(1, 9):
            self.update_board(Pawn('b', i, 7, '♟'))

    def update_board(self, piece):
        x, y = piece.x, piece.y
        self.board[self.convert(x,y)] = piece
    
    def convert(self, x, y):
        algebraic_x = chr(ord('a') + x - 1)
        return algebraic_x, y
    
    def convert_to_tuple(self, algebraic_x, algebraic_y):
    
        x = ord(algebraic_x) - ord('a') + 1
        # Convert algebraic_y to integer
        y = int(algebraic_y)
        return x, y
    def get_x_y(self, pos):
        x_line = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        return x_line.index(pos[0]) + 1, int(pos[1])

    def check_barriers(self, from_, to_, moves):
        x1, y1 = self.get_x_y(from_)
        x2, y2 = self.get_x_y(to_)
        
        if x1 == x2:
            for y in range(min(y1, y2) + 1, max(y1, y2)):
                if self.board[(self.x_line[x1-1], y)]:
                    return False
        elif y1 == y2:
            for x in range(min(x1, x2) + 1, max(x1, x2)):
                if self.board[(self.x_line[x-1], y1)]:
                    return False
        elif abs(x1 - x2) == abs(y1 - y2):
            x_step = 1 if x1 < x2 else -1
            y_step = 1 if y1 < y2 else -1
            x, y = x1 + x_step, y1 + y_step
            while (x, y) != (x2, y2):
                if self.board[(self.x_line[x-1], y)]:
                    return False
                x += x_step
                y += y_step

        return True

    def make_move(self, from_, to_):
        piece = self.board[from_]
        if piece is None:
            return False

        if self.convert_to_tuple(to_[0], to_[1]) not in piece.get_moves():
            return False

        if not self.validate_move(from_, to_):
            return False
        
        self.board[to_] = self.board[from_]
        self.board[from_] = None
        self.board[to_].x = to_[0]
        self.board[to_].y = to_[1]

        return True
    
    def validate_move(self, from_, to_):
        piece = self.board[from_]
        enemy = self.board[to_]
        if not piece:
            return False
        moves = piece.get_moves()

        if isinstance(piece, (Rook, Pawn, Bishop, Queen)):
            barriers = self.check_barriers(from_, to_, moves)
        else:
            barriers = True

        return (
            barriers
            and self.convert_to_tuple(to_[0], to_[1]) in moves
            and isinstance(piece, Piece)
            and (enemy is None or piece.color != enemy.color)
        )
    
    def print_board(self):

        for y in range(8, 0, -1):
            for x in 'abcdefgh':
                piece = self.board.get((x, y))
                if piece is None:
                    print('.', end=' ') 
                else:
                    print(piece.symbol, end=' ')  
            print()  

def get_x_y(pos):
    x_line = 'abcdefgh'
    return x_line.index(pos[0]) + 1, int(pos[1])

if __name__ == '__main__':
    g = ChessBoard()
    g.print_board()
    while True:
        from_pos, to_pos = input('from='), input('to=')
        g.make_move((from_pos[0], int(from_pos[1])),(to_pos[0], int(to_pos[1])))
        
        
        g.print_board()

