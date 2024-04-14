from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from game import Game
import json

app = FastAPI()
board = Game()

abc = 'abcdefgh'


def get_pos(x, y):
    return f'{abc[x - 1]}{y}'


def get_x_y(pos):
    return abc.index(pos[0]) + 1, int(pos[1])

@app.get("/show_board_console")
def show_board_console():
    return {"board": board.get_board_string()}


@app.get("/show_board", response_class=HTMLResponse)
def show_board():
    board_html = "<table>"
    l = list(board.board.values())
    l = ['_' if not i else i for i in l]
    l = [l[i : i + 8] for i in range(0, 64, 8)]
    for i, row in enumerate(l):
        board_html += "<tr>"
        for j, square in enumerate(row):
            cell_name = get_pos(j+1, 8-i)
            board_html += f"<td>{cell_name}: {square}</td>"
        board_html += "</tr>"
    board_html += "</table>"
    return board_html


@app.put("/make_move/{from_}/{to_}/")
def move(from_: str, to_: str):
    if board.make_move(from_, to_):  # Changed this line
        return {"Respose": "Scs"}

    return {'Respose': 'Bad'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)