EMPTY = ' '

FALLER_STOPPED = 0
FALLER_MOVING = 1

MOVE_DOWN  = 0
MOVE_LEFT  = -1
MOVE_RIGHT = 1

def _maximum(a, b):
     
    if a >= b:
        return a
    else:
        return b

class Faller:
    def __init__(self):
        '''
        Constructs a new faller object and initializes all the values
        '''
        self.active = False
        self._row = 0
        self._col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = FALLER_MOVING
        self.inbounds = False
        self.valid = True

    def get_row(self) -> int:
        return self._row

    def get_col(self) -> int:
        return self._col

    def set_row(self, row: int) -> None:
        self._row = row

    def set_col(self, col: int) -> None:
        self._col = col

    def find_bound(self) -> bool:
        return self.inbounds

    def rotate(self) -> None:
        if self.state == FALLER_MOVING:
            jewelOne = self.contents[2]
            jewelTwo = self.contents[0]
            jewelThree = self.contents[1]
            self.contents = [jewelOne, jewelTwo, jewelThree]


# State of a cell
EMPTY_CELL = 0
FALLER_MOVING_CELL = 1
FALLER_STOPPED_CELL = 2
OCCUPIED_CELL = 3
MATCHED_CELL = 4

class GameState:
    def __init__(self, columns: int, rows: int):
        '''
        Constructs a new GameState with a board that is the given (columns, rows)
        '''
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

    def add_content(self, contentRow: int, content: list) -> None:
        for row in range(self._rows):
            for col in range(self._columns):
                if contentRow == row:
                    self._board[col][row] = content[col]
                    if content[col] != ' ':
                        self._boardState[col][row] = OCCUPIED_CELL
                    else:
                        self._boardState[col][row] = EMPTY_CELL

    def columns(self) -> int:
        return self._columns

    def rows(self) -> int:
        return self._rows

    def get_board(self):
        return self._board

    def get_cell_state(self, col: int, row: int) -> int:
        try:    
            return self._boardState[col][row]
        except:
            None

    def set_cell_state(self, col: int, row: int, state: int) -> None:
        if row < 0:
            return
        self._boardState[col][row] = state

    def apply_gravity(self) -> None:
        for iter in range(0, self.rows()):
            for row in range(iter, self.rows()+1):
                for col in range(self.columns()):
                    if self._board[col][-(row)+1] == ' ' and self._board[col][-(row)] != ' ' and (-(row)+1) != 0:
                        jewel = self._board[col][-(row)]
                        self._board[col][-(row)+1] = jewel
                        self._board[col][-(row)] = ' '
                        self._boardState[col][-(row)+1] = OCCUPIED_CELL
                        self._boardState[col][-(row)] = EMPTY_CELL
        
    def do_matching(self) -> None:
        if self._faller.active == False:
            matching = False
            # First thing we do is get rid of any cells that are marked as matched from the previous tick
            for row in range(self.rows()):
                for col in range(self.columns()):
                    if self.get_cell_state(col, row) == MATCHED_CELL:
                        matching = True
                        self._board[col][row] = EMPTY
                        self.set_cell_state(col, row, EMPTY_CELL)                    
                        
            # Then apply gravity so everything moves down again  

            jewel = EMPTY
            for col in range(self.columns()):
                for row in range (self.rows()):
                    self._matching_begins(col, row)
            if matching == True:
                self.apply_gravity()
            matching = False
                        

    def get_faller(self) ->Faller:
        return self._faller

    def create_faller(self, column: int, faller_contents: list) -> None:
        '''
        Creates a faller in the given column and the given contents
        '''
        if self._faller.active:
            return

        self._faller.active = True
        self._faller.contents = faller_contents
        self._faller.set_row(0)
        self._faller.set_col(column - 1)
        self._faller.inbounds = False
        # Display the first cell of the faller
        self._board[self._faller.get_col()][0] = self._faller.contents[0]
        self.set_cell_state(self._faller.get_col(), 0, FALLER_MOVING_CELL)        

        # Check if the bottom row immediately under the faller
        self._update_faller_board_state()

    def rotate_faller(self) -> None:
        self._faller.rotate()
        self._update_faller_board_state()

    def game_tick(self) -> bool:
        '''
        Ticks one time unit for the game. This causes fallers to move down 
        '''
        if not self._faller.inbounds:
            self._faller.valid = False
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
                    if not self._faller.valid:
                        return 'over'
                    self.do_matching()
                    return value

            # If the faller is still in moving, move it down
            self.move_faller_down()

        # Handle matching and apply gravity
        self.do_matching()
        return False

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
        if self._faller._row >= 2:
            self._faller.inbounds = True
            self._faller.valid = True

    def move_faller_right(self) -> None:
        # Check if the next cell of faller has collision with other cell or ground
        if (self._has_collision(self._faller.get_col() + 1, self._faller.get_row())):
            return
        
        # Move the bottom row of faller down
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_RIGHT)
        # Move the middle row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_RIGHT)
        # Move the top row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_RIGHT)
        
        
        # Set the faller down one row (row number increase one)
        self._faller.set_col(colOfFaller + 1)
        self._update_faller_board_state()

    def move_faller_left(self) -> None:
        # Check if the next cell of faller has collision with other cell or ground
        if (self._has_collision(self._faller.get_col() - 1, self._faller.get_row())):
            return
        
        # Move the bottom row of faller down
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_LEFT)
        # Move the middle row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_LEFT)
        # Move the top row of faller down
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_LEFT)
        
        
        # Set the faller down one row (row number increase one)
        if colOfFaller > 0:
            self._faller.set_col(colOfFaller - 1)
            self._update_faller_board_state()

    def _update_faller_board_state(self) -> None:
        '''
        Updates the state of the faller according to its current conditions.
        If the faller reaches the bottom row then the state is set to FALLER_STOPPED.
        Otherwise the state is set to FALLER_MOVING.
        The cells of the faller on the board are updated as well.
        '''
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
            try:
                self._board[self._faller.get_col()][row] = self._faller.contents[inx]
                self.set_cell_state(self._faller.get_col(), row, state)
            except:
                self._faller._col = self._faller._col - 1

    def _has_collision(self, col: int, row: int) -> bool:
        '''
        Checks if a cell of the given row and column has collision (touch occupied cell or the bottom row)
        :return: True if the given cell has collision. False otherwise
        '''
        # The given row is below the bottom row
        if row >= self.rows():
            return True

        if self.get_cell_state(col, row) == OCCUPIED_CELL:
            return True

        return False
        
    def _move_cell(self, col: int, row: int, direction: int) -> None:
        '''
        Moves a cell in the given direction
        '''
        if direction == MOVE_DOWN:
            toRow = row + 1
            if (toRow >= self.rows() or toRow < 0):
                return

            oldValue = self._board[col][row]
            oldState = self._boardState[col][row]

            self._board[col][toRow] = oldValue
            self._boardState[col][toRow] = oldState

        elif direction == MOVE_RIGHT:
            toCol = col + 1
            if (toCol >= self.columns() or toCol < 0):
                return

            oldValue = self._board[col][row]
            oldState = self._boardState[col][row]

            self._board[toCol][row] = oldValue
            self._boardState[toCol][row] = oldState

        elif direction == MOVE_LEFT:
            toCol = col - 1
            if (toCol >= self.columns() or toCol < 0):
                return

            oldValue = self._board[col][row]
            oldState = self._boardState[col][row]

            self._board[toCol][row] = oldValue
            self._boardState[toCol][row] = oldState          
        if row > -1:
            self._board[col][row] = EMPTY
            self._boardState[col][row] = EMPTY_CELL
    
    def _matching_jewels(self, col: int, row: int, coldelta: int, rowdelta: int) -> bool:
        start_cell = self._board[col][row]

        if start_cell == EMPTY:
            return False
        else:
            for i in range(1, 3):
                if not self._valid_column(col + coldelta * i) \
                        or not self._valid_row(row + rowdelta * i) \
                        or self._board[col + coldelta *i][row + rowdelta * i] != start_cell:
                    return False
            # This direction has matching, mark the cells as 'MATCHED_CELL'
            # and continue to match until not satisfy the matching considtion
            self.set_cell_state(col, row, MATCHED_CELL)
            for i in range(1, 3):
                self.set_cell_state(col + coldelta *i, row + rowdelta * i, MATCHED_CELL)
            largestNum = _maximum(self.rows() - rowdelta, self.columns() - coldelta)
            if (largestNum >= 4):
                for i in range(4, largestNum):
                    if self._valid_column(col + coldelta * i) \
                        and self._valid_row(row + rowdelta * i) \
                        and self._board[col + coldelta *i][row + rowdelta * i] == start_cell:
                        self.set_cell_state(col + coldelta *i, row + rowdelta * i, MATCHED_CELL)

            return True
    
    def _valid_column(self, column_number: int) -> bool:
        return 0 <= column_number < self.columns()

    def _valid_row(self, row_number: int) -> bool:
        return 0 <= row_number < self.rows()
    
    def _matching_begins(self, col: int, row: int) -> bool:
        return self._matching_jewels(col, row, 0, 1) \
                or self._matching_jewels(col, row, 1, 1) \
                or self._matching_jewels(col, row, 1, 0) \
                or self._matching_jewels(col, row, 1, -1) \
                or self._matching_jewels(col, row, 0, -1) \
                or self._matching_jewels(col, row, -1, -1) \
                or self._matching_jewels(col, row, -1, 0) \
                or self._matching_jewels(col, row, -1, 1)