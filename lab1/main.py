board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
]

# Виводимо ігрове поле
def show_board():
    for row in board:
        print('| {0} | {1} | {2} |'.format(*row))
        print('-------------')

# Перевірка на виграш
def is_winning(board, symbol):
    # перевіряємо рядки
    for row in board:
        if all(cell == symbol for cell in row):
            return True

    # перевіряємо стрічки
    for i in range(3):
        if all(board[j][i] == symbol for j in range(3)):
            return True

    # перевіряємо діагоналі
    return (
        all(board[i][i] == symbol for i in range(3)) or
        all(board[i][2 - i] == symbol for i in range(3))
    )

# хід гравця
def get_move(symbol):
    while True:
        x = int(input('Стрічка (0, 1, 2): '))
        y = int(input('Колонка(0, 1, 2): '))

        # перевірка на валідність інпута
        if not 0 <= x < 3 or not 0 <= y < 3:
            continue

        # перевірка чи достпна клітинка
        if board[x][y] != ' ':
            continue

        return x, y


def show_turn(turn):
    print('Черга ходити {}'.format(turn))

def is_board_full(board):
    # Перевірка чи все запонено
    for row in board:
        for cell in row:
            if cell == ' ':
                return False
    return True

# Start
turn = 'X'
while True:
    show_board()
    show_turn(turn)

    # Отримати хід гравця
    x, y = get_move(turn)

    # Отримати хід гравця
    board[x][y] = turn

    # Перевірити виграш чи нічию
    if is_winning(board, turn):
        print('{} вигра!'.format(turn))
        break
    elif is_board_full(board):  # Перевірити нічию
        print('Нічия!')
        break

    # Міняємо чергу
    turn = 'O' if turn == 'X' else 'X'


# Зробити нічию
if not is_winning(board, 'X') and not is_winning(board, 'O'):
    print('Нічия!')
