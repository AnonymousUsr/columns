
EMPTY = ' '
JEWEL1 = 1
JEWEL2 = 2
JEWEL3 = 3
JEWEL4 = 4
JEWEL5 = 5
JEWEL6 = 6
JEWEL7 = 7

FALLER_STOPPED = 0
FALLER_MOVING = 1


class Faller:
    def __init__(self):
        """
        Constructs a new faller object and initializes all the values
        """
        self.active = False
        self._row = 0
        self._col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = FALLER_MOVING

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def set_row(self, row: int) -> None:
        self._row = row

    def set_col(self, col: int) -> None:
        self._col = col

    def rotate(self) ->None:
        pass


# State of a cell
EMPTY_CELL = 0
FALLER_MOVING_CELL = 1
FALLER_STOPPED_CELL = 2
OCCUPIED_CELL = 3
MATCHED_CELL = 4

class GameState:
    def __init__(self, columns: int, rows: int):
        """
        Constructs a new GameState with a board that is the given (columns, rows)
        """
        super().__init__()
        self._rows = rows
        self._columns = columns
        self._board = []
        self._boardState = []
        self._faller = Faller()
        self.new_game(columns, rows)

    def new_game(self, columns: int, rows: int) -> None:
        for col in range(columns):
            self._board.append([])
            self._boardState.append([])
            for row in range(rows):
                self._board[-1].append(EMPTY)
                self._boardState[-1].append(EMPTY_CELL)

    def columns(self) -> int:
        return self._columns

    def rows(self) -> int:
        return self._rows

    def get_board(self):
        return self._board

    def get_cell_state(self, col: int, row: int) -> int:
        return self._boardState[col][row]

    def set_cell_state(self, col: int, row: int, state: int) -> None:
        if row < 0:
            return
        self._boardState[col][row] = state

    def set_board_contents(self, contents: [[str]]) -> None:
        """
        Sets the contents of the board to the given contents, then applies gravity and attempts matching
        """
        for row in range(self.rows()):
            for col in range(self.columns()):
                value = contents[row][col]
                if value == ' ':
                    self._board[col][row] = EMPTY
                    self._boardState[col][row] = EMPTY_CELL
                else:
                    self._board[col][row] = value
                    self._boardState[col][row] = OCCUPIED_CELL

        #self.apply_gravity()
        #self.do_matching()

    def get_faller(self) ->Faller:
        return self._faller

    def create_faller(self, column: int, falle_contents: []) -> None:
        """
        Creates a faller in the given column and the given contents
        """
        if self._faller.active:
            return

        self._faller.active = True
        self._faller.contents = falle_contents
        self._faller.set_row(0)
        self._faller.set_col(column - 1)

    def move_faller_side(self) ->None:
        pass

    def move_faller_down(self) ->None:
        pass

        
