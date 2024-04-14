from fastapi import FastAPI
from fastapi.responses import JSONResponse 
from game import ChessBoard
from piece import Piece

app = FastAPI()
board = ChessBoard()


def get_x_y(pos):
    x_line = 'abcdefgh'
    return x_line.index(pos[0]) + 1, int(pos[1])

@app.get("/board")
def get_board():
    board_state = [{"pos": position, "p": piece} for position, piece in board.board.items()]
    return board_state
    

@app.put("/move/{from_pos}/{to_pos}")
def move_piece(from_pos: str, to_pos: str):
    # from_x, from_y = get_x_y(from_pos)
    # to_x, to_y = get_x_y(to_pos)

    board.make_move((from_pos[0], int(from_pos[1])),(to_pos[0], int(to_pos[1])))
    board.print_board()
    return {"message": "Successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)