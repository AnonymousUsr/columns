import columns_functions

def input_results():
    rows = input('')
    columns = input('')
    userInput = input('')
    if userInput.upper() == 'Q':
        return 'done'
    elif userInput.upper() == 'EMPTY':
        game = columns_functions.GameState(int(columns), int(rows))
        print_board(game)
        return game
    while True:
        userInput = input('')
        if userInput[0].upper() == 'F':
            None
        elif userInput == '':
            None
        elif userInput == 'R':
            None
        elif userInput == '<':
            None
        elif userInput == '>':
            None
        elif userInput == 'Q':
            None

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
                elif cellState == columns_functions.MATCHED_CELL:
                    print('*{}*'.format(jewel), end = '')
        print('|')
    print(' ', end = '')
    for numbers in range(0, numOfColumns):
        print('---', end = '')
    print(' ')


if __name__ == '__main__':
    input_results()
