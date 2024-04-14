#Кількість клітинок
size_board = 3





#Індекси на ігровому полі
board = [1, 2, 3, 4, 5, 6, 7, 8, 9]

#Малюнок поля
def painting_board():
    print('_' * 4 * size_board)
    for i in range(size_board):
        print((' ' * 3 + '|') * 3 )
        print('', board[i * 3], '|', board[1 + i*3], '|', board[2 + i*3], '|')
        print(('_' * 3 + '|') * 3 )

        

#Хід
def game_step(index, char): 
    
    if (index > 9 or index < 1 or board[index - 1] in ('X', 'O')):
        return false
    
    board[index - 1] = char
    return True
#Перевірка чи хтось не переміг 
def check_win():
    
    win = False
    
    win_combination = (
        (0,1,2), (3,4,5), (6,7,8),      #Горизонтальні лінії
        (0,3,6), (1,4,7), (2,5,8),      #Вертикальні лінії 
        (0,4,8), (2,4,6)                #Діагональні лінії
    )
    
    for pos in win_combination:
        if (board[pos[0]] == board[pos[1]] and board[pos[1]] == board[pos[2]]): 
            win = board[pos[0]]
    
    return win

#Початок гри
def start_game():
    #Поточний гравець
    current_player = 'X'
    #Номер ходу
    step = 1
    painting_board() 

    while (step < 10) and (check_win() == False):
    
        index = input('the move ' + current_player + '. Enter the field number (0 - exit):')      
            
        if (index == '0'):
            break

        #Якщо получилось зробити хід 
        if (game_step(int(index), current_player)):
            print('The move is completed')
        
            if (current_player == 'X'):
                current_player = 'O'
            else:
                current_player = 'X'           
            
            
            
            painting_board()
            #Збільшуємо номер ходу
            step += 1
        else:
            print('Try again')
    if (step == 10):
        print('Draw')
    
    print('Wining ' + check_win())        
print("Game Start")
start_game()







