from pieces import Pawn, King, Knight, Rook, Bishop, Queen, Piece

class Chess:
    def __init__(self):
        self.board = {}
        self.setup()

    def setup(self):
        for x in range(1,9):
            self.board[(x, 2)] = Pawn(x, 2,"w")
            self.board[(x, 7)] = Pawn(x, 7, 'b')
        
        pieces_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for y, color in zip([1, 8], ["w", "b"]):
            for x, piece_class in enumerate(pieces_order):
                self.board[(x+1, y)] = piece_class(x+1, y, color)

        for x in range(1,9):
            for y in range(3, 7):
                self.board[(x, y)] = None
                
        return self.board
    
    def validate_move(self, from_, to_, moves):
        piece = self.board[from_]
        destination_piece = self.board[to_]

        if destination_piece and destination_piece.color == piece.color:
            return False

        if not isinstance(piece, (Rook, Pawn, Bishop, Queen)):
            return True

        dx = 1 if to_[0] > from_[0] else -1 if to_[0] < from_[0] else 0
        dy = 1 if to_[1] > from_[1] else -1 if to_[1] < from_[1] else 0
        
        x, y = from_
        while (x, y) != to_:
            x += dx
            y += dy
            
            if self.board.get((x, y)):
                return False
            if (x, y) in moves:
                return True
            
        return True
    
    def move(self, from_x_y, to_x_y):
        piece = self.board[from_x_y]
        if piece is None:
            return False
        moves = [(from_x_y[0] + x, from_x_y[1] + y) for x,y in piece.get_moves()]

        if to_x_y in moves and self.validate_move(from_x_y, to_x_y, moves):
            self.board[to_x_y] = piece
            self.board[from_x_y] = None
            return True
        else:
            return False
    
    def print_board(self):
        for y in range(1, 9):
            for x in range(1, 9):
                if self.board[(x, y)]:
                    print(self.board[(x, y)], end=" ")
                else:
                    print('_', end=" ")
            print()
        






