
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

MOVE_DOWN  = 0
MOVE_LEFT  = -1
MOVE_RIGHT = 1

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
        # Display the first cell of the faller
        self._board[self._faller.get_col()][0] = self._faller.contents[0]
        self.set_cell_state(self._faller.get_col(), 0, FALLER_MOVING_CELL)        

        # Check if the bottom row immediately under the faller
        self._update_faller_board_state()

    def game_tick(self) -> bool:
        """
        Ticks one time unit for the game. This causes fallers to move down 
        """
        # Handle the faller first
        if self._faller.active:
            
            if self._faller.state == FALLER_STOPPED:
                # Do another update on the faller state to see what state it is now 
                self._update_faller_board_state()
                # If the faller is still stopped after the update then freeze it
                if self._faller.state == FALLER_STOPPED:
                    value = False

                    # freeze the faller cells on the board
                    for inx in range(3):
                        row = self._faller.get_row() - inx
                        if (row >= 0):
                            self._board[self._faller.get_col()][row] = self._faller.contents[inx]
                            self.set_cell_state(self._faller.get_col(), row, OCCUPIED_CELL)
                    self._faller.active = False

                    #self.do_matching()
                    return value

            # If the faller is still in moving, move it down
            self.move_faller_down()

        # Handle matching and apply gravity
        # self.do_matching()
        return False

    def move_faller_side(self) ->None:
        pass

    def move_faller_down(self) ->None:
        # Check if the next cell of faller has collision with other cell or ground
        if (self._has_collision(self._faller.get_col(), self._faller.get_row() + 1)):
            return
        
        # Move the bottom row of faller down
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_DOWN)
        # Move the middle row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_DOWN)
        # Move the top row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_DOWN)
        
        # Set the faller down one row (row number increase one)
        self._faller.set_row(rowOfFaller + 1)
        self._update_faller_board_state()

    def _update_faller_board_state(self) -> None:
        """
        Updates the state of the faller according to its current conditions.
        If the faller reaches the bottom row then the state is set to FALLER_STOPPED.
        Otherwise the state is set to FALLER_MOVING.
        The cells of the faller on the board are updated as well.
        """
        state = None
        toRow = self._faller.get_row() + 1
        if self._has_collision(self._faller.get_col(), toRow):
            state = FALLER_STOPPED_CELL
            self._faller.state = FALLER_STOPPED
        else:
            state = FALLER_MOVING_CELL
            self._faller.state = FALLER_MOVING

        for inx in range(3):
            row = self._faller.get_row() - inx
            if row < 0:
                return

            # Update board cell
            self._board[self._faller.get_col()][row] = self._faller.contents[inx]
            self.set_cell_state(self._faller.get_col(), row, state)

    def _has_collision(self, col: int, row: int) -> bool:
        """
        Checks if a cell of the given row and column has collision (touch occupied cell or the bottom row)
        :return: True if the given cell has collision. False otherwise
        """
        # The given row is below the bottom row
        if row >= self.rows():
            return True

        if self.get_cell_state(col, row) == OCCUPIED_CELL:
            return True

        return False
        
    def _move_cell(self, col: int, row: int, direction: int) -> None:
        """
        Moves a cell in the given direction
        """
        if direction == MOVE_DOWN:
            toRow = row + 1
            if (toRow >= self.rows() or toRow < 0):
                return

            oldValue = self._board[col][row]
            oldState = self._boardState[col][row]

            self._board[col][toRow] = oldValue
            self._boardState[col][toRow] = oldState
        else:
            # direction = MOVE_RIGHT (+1) MOVE_LEFT(-1)
            toCol = col + direction
            if (toCol >= self.columns() or toCol < 0):
                return

            oldValue = self._board[col][row]
            oldState = self._boardState[col][row]

            self._board[toCol][row] = oldValue
            self._boardState[toCol][row] = oldState        

        self._board[col][row] = EMPTY
        self._boardState[col][row] = EMPTY_CELL

