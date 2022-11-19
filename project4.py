import columns_functions

def input_results():
    rows = input('')
    columns = input('')
    userInput = input('')
    if userInput.upper() == 'Q':
        return 'done'
    elif userInput.upper() == 'EMPTY':
        game = columns_functions.new_game(int(columns), int(rows))
        columns_functions.print_board(game)
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

if __name__ == '__main__':
    input_results()
