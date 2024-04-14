

class Piece:
    name = None
    def __init__(self, x, y,color):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self) -> str:
        return str(self.name)


class Pawn(Piece):
    moved = False
    name = 'p'

    def get_moves(self):
        l = []
        for x, y in [(0, 1), (0, 2)]:
            if self.color == 'b':
                y *= -1
            if self.moved:
                l += [(x,y),]
                break
            else:
                l += [(x,y)]
        
        return l
    
class King(Piece):
    name = 'k'

    def get_moves(self):
        moves = []
        for x in range(-1, 2):
            for y in range(-1,2):
                moves.append((x,y))

        return moves

class Rook(Piece):
    name = 'r'

    def get_moves(self):
        moves = []
        
        for i in range(1, 9):
            if self.x + i <= 8:
                moves.append((i, 0))

            if self.x - i - 1 >= 0:
                moves.append((i*-1, 0))

        for i in range(1, 9):
            if self.y + i <= 8:
                moves.append((0, i))

            if self.y - i - 1 >= 0:
                moves.append((0, i*-1))

        
        return moves


class Bishop(Piece):
    name = 'b'

    def get_moves(self):
        moves = []

        for i in range(1, min(8 - self.x, 8 - self.y) + 1):
            moves.append((i, i))

        for i in range(1, min(self.x - 1, self.y - 1) + 1):
            moves.append((-i, -i))

        for i in range(1, min(self.x - 1, 8 - self.y) + 1):
            moves.append((-i, i))

        for i in range(1, min(8 - self.x, self.y - 1) + 1):
            moves.append((i, -i))


        return moves

class Queen(Piece):
    name = 'q'
    
    def get_moves(self):
        b = Bishop.get_moves(self)
        r = Rook.get_moves(self)
        return r + b
    
class Knight(Piece):
    name = 'kn'

    def get_moves(self):
        knight_moves = []
        for x in range(-2, 3):
            for y in range(-2, 3):
                if abs(x) + abs(y) == 3:
                    if 1 <= self.x + x <= 8 and 1 <= self.y + y <= 8:  
                        knight_moves.append((x, y))  

        return knight_moves
        




if __name__ == '__main__':
    p = King(1,1, 'b',)
    print(p.get_moves())