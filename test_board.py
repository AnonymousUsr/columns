import columns_functions
from project4 import print_board

def test_empty_board():
    game = columns_functions.GameState(3, 4)
    contents = [
        [' ', ' ', 'Y', 'X'],
        ['S', ' ', 'V', ' '],
        ['T', 'X', 'Y', 'S'],
        ['X', ' ', 'X', 'Y']
    ]

    game.set_board_contents(contents)
    game.set_cell_state(0, 2, columns_functions.FALLER_MOVING_CELL)
    print_board(game)


if __name__ == '__main__':
    test_empty_board()