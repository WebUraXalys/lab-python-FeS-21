from fastapi import FastAPI
from chess import Chess

app = FastAPI()
board = Chess()

abc = 'abcdefgh'

def get_pos(x, y):
    return f'{abc[x - 1]}{y}'

def get_x_y(pos):
    return abc.index(pos[0]) + 1, int(pos[1])

@app.get("/board")
def show_board():
    d = {}    
    for pos, piece in board.board.items():
        if piece:
            p = {'name': piece.name, 'color': piece.color}
        else:
            p = None
        
        d[f'{get_pos(pos[0], pos[1])}'] = p

    return d

    


@app.put("/move/{from_}/{to_}/")
def move(from_:str,to_:str):
    if board.move(get_x_y(from_), get_x_y(to_)):
        board.print_board()
        return {"Ok": "Ok"}
    else:
        return {'Bad': 'bad'}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)