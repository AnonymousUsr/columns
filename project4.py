import columns_functions

def input_results():
    rows = input('')
    columns = input('')
    userInput = input('')
    if userInput.upper() == 'Q':
        return 'over'
    elif userInput.upper() == 'EMPTY':
        game = columns_functions.GameState(int(columns), int(rows))
        print_board(game)
    elif userInput.upper() == 'CONTENTS':
        game = columns_functions.GameState(int(columns), int(rows))
        for num in range(int(rows)):
            contentInput = input('')
            splitInput = split_string(contentInput)
            if len(splitInput) != int(columns):
                return 'error'
            game.add_content(num, splitInput)
        game.apply_gravity()
        game.do_matching()
        print_board(game)
    else:
        return 'error'
    while True:
        userInput = input('')
        if userInput.upper().strip() == 'Q':
            return 'over'
        elif userInput.strip() == '':
            result = game.game_tick()
            if result == 'over':
                return game
        elif userInput[0].upper() == 'F':
            tempList = []
            tempSplit = userInput.split(' ')
            for item in tempSplit[2:]:
                if type(item) == 'String':
                    item = item.upper()
                tempList.append(item)
            tempList.reverse()
            game.create_faller(int(tempSplit[1]), tempList)
        elif userInput.upper().strip() == 'R':
            game.rotate_faller()
        elif userInput == '<':
            game.move_faller_left()
        elif userInput == '>':
            game.move_faller_right()
        else:
            print('Invalid command.')
        print_board(game)

def print_board(game_state: columns_functions.GameState) -> None:
    '''Prints out the board of a connect four game
    Parameter - connectfour GameState
    Return - none, prints out the board of the connect four game'''
    numOfColumns = game_state.columns()
    numOfRows = game_state.rows()
    formatBoard = format('{block:>2}')
    formatJewels = format('{block:^1}')
    board = game_state.get_board()
    for row in range(0, numOfRows):
        print('|', end = '')
        for column in range(0, numOfColumns):
            if board[column][row] == ' ':
                print(formatBoard.format(block = ' '), end = ' ')
            else:
                jewel = board[column][row]
                cellState = game_state.get_cell_state(column, row)
                if cellState == columns_functions.OCCUPIED_CELL:
                    print(formatBoard.format(block = jewel), end = ' ')
                elif cellState == columns_functions.FALLER_MOVING_CELL:
                    print('[{}]'.format(jewel), end = '')
                elif cellState == columns_functions.FALLER_STOPPED_CELL:
                    print('|{}|'.format(jewel), end = '')
                    pass
                elif cellState == columns_functions.MATCHED_CELL:
                    print('*{}*'.format(jewel), end = '')
                    pass                
        print('|')
    print(' ', end = '')
    for numbers in range(0, numOfColumns):
        print('---', end = '')
    print(' ')

def split_string(text: str) -> list:
    returnList = []
    for char in text:
        returnList.append(char)
    return returnList

if __name__ == '__main__':
    results = input_results()
    if results == 'over':
        None
    elif results == 'error':
        print('ERROR')
    else:
        print_board(results)
        print('GAME OVER')
