class Piece:
    def __init__(self, color, x, y, _type, name, symbol=None, ):
        self.color = color  
        self.x = x  
        self.y = y  
        self._type = _type
        self.symbol = symbol
        self.name = name
        self.position = self.get_pos(x, y)

    def __repr__(self) -> str:
        return self._type
    
    def info(self):
        return self.__dict__

    def get_cords(self):
        return (self.x_coord, self.y_coord)
    
    def get_pos(self, x, y):
        x_line = 'abcdefgh'
        return f'{x_line[x - 1]}{y}'
    
    def check_border(self, x, y):
        return 1 <= x <= 8 and 1 <= y <= 8


class Pawn(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'p', 'Rook', symbol)
        self.moved = False  # Flag to track if the pawn has moved before

    def get_moves(self):
        if self.color == 'w':
            available_moves = [(0, 1), (0, 2)]
            if self.moved:
                available_moves = [(0, 1)]


        if self.color == 'b':
            available_moves = [(0, -1), (0, -2)]
            if self.moved:
                available_moves = [(0, -1)]
        moves = []
        for x, y in available_moves:
            moves.append((self.x + x, self.y + y))
        return moves



class Rook(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'r', 'Rook', symbol)

    def get_moves(self):
        moves = []

        # Check vertical moves (upwards)
        for i in range(self.y + 1, 9):
            moves.append((self.x, i))

        # Check vertical moves (downwards)
        for i in range(self.y - 1, 0, -1):
            moves.append((self.x, i))

        # Check horizontal moves (to the right)
        for j in range(self.x + 1, 9):
            moves.append((j, self.y))

        # Check horizontal moves (to the left)
        for j in range(self.x - 1, 0, -1):
            moves.append((j, self.y))

        return moves


class Bishop(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'b', 'Bishop', symbol)

    def get_moves(self):
        moves = []

        # Check diagonal moves (up-right)
        for i in range(1, min(8 - self.x, 8 - self.y) + 1):
            moves.append((self.x + i, self.y + i))

        # Check diagonal moves (up-left)
        for i in range(1, min(self.x - 1, 8 - self.y) + 1):
            
    
            moves.append((self.x - i, self.y + i))

        # Check diagonal moves (down-right)
        for i in range(1, min(8 - self.x, self.y - 1) + 1):
            moves.append((self.x + i, self.y - i))

        # Check diagonal moves (down-left)
        for i in range(1, min(self.x - 1, self.y - 1) + 1):
            moves.append((self.x - i, self.y - i))

        return moves


class Queen(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'q', 'Queen', symbol)

    def get_moves(self):
        r = Rook(self.color, self.x, self.y, self.symbol).get_moves()
        b = Bishop(self.color, self.x, self.y, self.symbol).get_moves()
        return r + b
        


class Knight(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'kn', 'Knight', symbol)

    def get_moves(self):
        moves = []

        # Define all possible knight moves relative to its current position
        knight_moves = [
            (2, 1), (1, 2), (-1, 2), (-2, 1),
            (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        # Check each potential move
        for move in knight_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            # Ensure the new position is within the board bounds (1-8)
            if self.check_border(new_x, new_y):
                moves.append((new_x, new_y))

        return moves



class King(Piece):
    def __init__(self, color, x, y, symbol):
        super().__init__(color, x, y, 'k', 'King', symbol)

    def get_moves(self):
        moves = []

        king_moves = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for move in king_moves:
            new_x = self.x + move[0]
            new_y = self.y + move[1]
            # Ensure the new position is within the board bounds (1-8)
            if self.check_border(new_x, new_y):
                moves.append((new_x, new_y))

        return moves


if __name__ == '__main__':
    pawn = Knight('w', 2, 1, None)
    print(pawn.get_moves())
