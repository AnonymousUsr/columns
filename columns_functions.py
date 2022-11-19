from collections import namedtuple

GameState = namedtuple('GameState', ['board', 'something'])

EMPTY = 0
JEWEL1 = 1
JEWEL2 = 2
JEWEL3 = 3
JEWEL4 = 4
JEWEL5 = 5
JEWEL6 = 6
JEWEL7 = 7

def find_jewel(jewel: int) -> str:
    if jewel == 0:
        return ' '
    elif jewel == 1:
        return 'S'
    elif jewel == 2:
        return 'T'
    elif jewel == 3:
        return 'V'
    elif jewel == 4:
        return 'W'
    elif jewel == 5:
        return 'X'
    elif jewel == 6:
        return 'Y'
    elif jewel == 7:
        return 'Z'


def new_game(columns: int, rows: int) -> GameState:
    board = []

    for col in range(columns):
        board.append([])
        for row in range(rows):
            board[-1].append(EMPTY)

    return GameState(board, something = '')

def columns(game_state: GameState) -> int:
    return len(game_state.board)

def rows(game_state: GameState) -> int:
    return len(game_state.board[0])

def print_board(game_state: GameState) -> None:
    '''Prints out the board of a connect four game
    Parameter - connectfour GameState
    Return - none, prints out the board of the connect four game'''
    numOfColumns = columns(game_state)
    numOfRows = rows(game_state)
    formatBoard = format('{block:>2}')
    formatJewels = format('{block:^1}')
    board, something = game_state
    for row in range(0, numOfRows):
        print('|', end = '')
        for column in range(0, numOfColumns):
            if board[column][row] == 0:
                print(formatBoard.format(block = '2'), end = ' ')
            else:
                jewel = board[column][row]
                print(formatBoard.format(block = find_jewel(jewel)), end = ' ')
        print('|')
    print(' ', end = '')
    for numbers in range(0, numOfColumns):
        print('---', end = '')
    print(' ')
