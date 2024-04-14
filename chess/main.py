from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from starlette.applications import Starlette
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
from enum import Enum
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class NameMapping(Enum):
    pawn = 1
    knight = 2
    bishop = 3
    rook = 4
    queen = 5
    king = 6

class Move(BaseModel):
    player: str
    position_from: str
    position_to: str

class Piece(BaseModel):
    color: str
    position: tuple


class King(Piece):
    pass


class Rook(Piece):
    pass


class Knight(Piece):
    pass


class Bishop(Piece):
    pass


class Queen(Piece):
    pass


class Pawn(Piece):
    def __init__(self, color: str, position: tuple):
        super().__init__(color=color, position=position)


class Board(BaseModel):
    pieces: List[List[str]] = [
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8,
        [""] * 8
    ]


class Game:
    def __init__(self):
        self.board = None
        self.current_player = None

    def start_game(self):
        self.board = self.initialize_board()
        self.current_player = "white"

    def initialize_board(self):
        board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P"] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            ["p"] * 8,
            ["r", "n", "b", "q", "k", "b", "n", "r"]
        ]
        return board

    def move(self, player: str, position_from: str, position_to: str):
        if player != self.current_player:
            raise ValueError("It's not your turn to move.")

        position_from = self.convert_position(position_from)
        position_to = self.convert_position(position_to)

        piece = self.board[position_from[0]][position_from[1]]
        if piece == "":
            raise ValueError("There is no piece at the specified position.")
        if piece.isupper() and player != "white" or piece.islower() and player != "black":
            raise ValueError("It's not your turn to move.")
        
        if not self.validate_move(player, position_from, position_to):
            raise ValueError("Invalid move.")
       
        self.board[position_to[0]][position_to[1]] = piece
        self.board[position_from[0]][position_from[1]] = ""
        self.current_player = "black" if self.current_player == "white" else "white"
        return {"message": "Move executed successfully"}

    def validate_move(self, player, position_from, position_to):
        piece = self.board[position_from[0]][position_from[1]]
        if piece.lower() == 'p':
            pawn = Pawn(color=piece.isupper(), position=position_from)
            return pawn_rule(pawn.color, self.board, *position_from, *position_to)
        return True

    def get_board(self):
        if self.board:
            return {"pieces": self.board}
        else:
            return {"pieces": []}

    def convert_position(self, position):
        columns = 'ABCDEFGH'
        row = int(position[1]) - 1
        col = columns.index(position[0].upper())
        return (row, col)


def pawn_rule(color, board, x, y, newx, newy):
    enemy_indexes = [(i)*color*-1 for i in range(1, 7)]
    if x != newx:  # attack
        if color == 1:
            if abs(newx-x) == 1 and y-newy == 1:
                if board[newy][newx] in enemy_indexes:
                    return True
        else:
            if abs(newx-x) == 1 and newy-y == 1:
                if board[newy][newx] in enemy_indexes:
                    return True

        return False
    else:  # move
        if color == 1:
            is_first_move = True if y == 2 else False

            if is_first_move and y-newy == 6 and board[newy][newx] == "" and board[newy+1][newx] == "":
                return True
            elif y-newy == 2 and board[newy][newx] == "":
                return True
        else:
            is_first_move = True if y == 1 else False

            if is_first_move and newy-y == 1 and board[newy][newx] == "" and board[newy-1][newx] == "":
                return True
            elif newy-y == 2 and board[newy][newx] == "":
                return True

        return False


def knight_rule(color, board, x, y, newx, newy):
    if not abs(x-newx) + abs(y-newy) == 3:
        return False
    if abs(x-newx) == 3 or abs(y-newy) == 3:
        return False

    friend_indexes = [(i)*color for i in range(1, 7)]

    if board[newy][newx] not in friend_indexes:
        return True


def bishop_rule(color, board, x, y, newx, newy):
    if (x == newx or y == newy):
        return False
    if abs(x-newx) != abs(y-newy):
        return False

    friend_indexes = [(i)*color for i in range(1, 7)]
    enemy_indexes = [(i)*color*-1 for i in range(1, 7)]

    x_sign = 1 if x < newx else -1
    y_sign = 1 if y < newy else -1

    for i in range(0, abs(x-newx), 1):
        if board[y+(i*y_sign)][x+(i*x_sign)] == "" or (y+(i*y_sign) == y and x+(i*x_sign) == x):
            continue
        if board[y+(i*y_sign)][x+(i*x_sign)] in enemy_indexes and i != abs(x-newx):
            return False
        if board[y+(i*y_sign)][x+(i*x_sign)] in friend_indexes:
            return False

    if abs(x-newx) == 1:
        if board[newy][newx] in friend_indexes:
            return False
        else:
            return True

    return True


def rook_rule(color, board, x, y, newx, newy):
    if not ((x == newx and y != newy) or (y == newy and x != newx)):
        return False

    friend_indexes = [(i)*color for i in range(1, 7)]
    enemy_indexes = [(i)*color*-1 for i in range(1, 7)]

    is_x_move = True if (y == newy and x != newx) else False

    if is_x_move:
        is_move_left = True if x - newx > 0 else False

        if is_move_left:
            for i in range(newx, x+1):
                if board[y][i] in friend_indexes and i != x:
                    return False
                if board[y][i] in enemy_indexes and i != newx:
                    return False
        else:
            for i in range(x, newx+1):
                if board[y][i] in friend_indexes and i != x:
                    return False
                if board[y][i] in enemy_indexes and i != newx:
                    return False
        return True
    else:
        is_move_up = True if y - newy > 0 else False

        if is_move_up:
            for i in range(newy, y+1):
                if board[i][x] in friend_indexes and i != y:
                    return False
                if board[i][x] in enemy_indexes and i != newy:
                    return False
        else:
            for i in range(y, newy+1):
                if board[i][x] in friend_indexes and i != y:
                    return False
                if board[i][x] in enemy_indexes and i != newy:
                    return False
        return True


def queen_rule(color, board, x, y, newx, newy):
    if bishop_rule(color, board, x, y, newx, newy) or rook_rule(color, board, x, y, newx, newy):
        return True
    return False


def king_rule(color, board, x, y, newx, newy):
    if (bishop_rule(color, board, x, y, newx, newy) or rook_rule(color, board, x, y, newx, newy)) \
            and (abs(newx-x) in (0, 1) and abs(newy-y) in (0, 1)):
        return True
    return False


RuleMapping = [
    None,
    pawn_rule,
    knight_rule,
    bishop_rule,
    rook_rule,
    queen_rule,
    king_rule,
]


# Instantiate the Game class
game = Game()

# API endpoints
@app.post("/start_game")
def start_game():
    game.start_game()
    return {"message": "Game started"}


@app.post("/move")
def move(move: Move):
    try:
        game.move(move.player, move.position_from, move.position_to)
        return {"message": "Move executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/end_game")
def end_game():
    game.end_game()
    return {"message": "Game ended"}


@app.get("/display_board", response_class=HTMLResponse)
def display_board(request: Request):
    board_state = game.get_board()
    return templates.TemplateResponse("board.html", {"request": request, "board_state": board_state})

@app.get("/")
def root():
    return {"message": "Welcome to Chess API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
