import random


class Cell:
    '''Represents a cell within a game of Sudoku.'''

    def __init__(self, row, col, value, editable):
        '''Initializes an instance of a Sudoku cell.'''
        self.row = row
        self.col = col
        self.value = value
        self._editable = editable

    @property
    def row(self):
        '''Getter method for row.'''
        return self._row

    @row.setter
    def row(self, row):
        '''Setter method for row.'''
        if row < 0 or row > 8:
            raise AttributeError('Row must be between 0 and 8.')
        else:
            self._row = row

    @property
    def col(self):
        '''Getter method for col.'''
        return self._col

    @col.setter
    def col(self, col):
        '''Setter method for col.'''
        if col < 0 or col > 8:
            raise AttributeError('Col must be between 0 and 8.')
        else:
            self._col = col

    @property
    def value(self):
        '''Getter method for value.'''
        return self._value

    @property
    def editable(self):
        '''Getter method for editable.'''
        return self._editable

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    @value.setter
    def value(self, value):
        '''Setter method for value.'''
        if value is not None and (value < 1 or value > 9):
            raise AttributeError('Value must be between 1 and 9.')
        else:
            self._value = value


class Sudoku:
    '''Represents a game/board of Sudoku.'''

    def __init__(self, board):
        '''Initializes an instance of a Sudoku game.'''
        self.board = []
        for row in range(9):
            self.board.append([])
            for col in range(9):
                if board[row][col] == 0:
                    val = None
                    editable = True
                else:
                    val = board[row][col]
                    editable = False
                self.board[row].append(Cell(row, col, val, editable))

    def check_move(self, cell, num):
        '''Returns whether a number is a valid move for a cell.'''
        # verification de la ligne
        for col in range(9):
            if self.board[cell.row][col].value == num and col != cell.col:
                return False

        #verification de la colonne
        for row in range(9):
            if self.board[row][cell.col].value == num and row != cell.row:
                return False

        # verification de la validité du chiffre
        for row in range(cell.row // 3 * 3, cell.row // 3 * 3 + 3):
            for col in range(cell.col // 3 * 3, cell.col // 3 * 3 + 3):
                if (
                    self.board[row][col].value == num
                    and row != cell.row
                    and col != cell.col
                ):
                    return False

        # le nb est valide
        return True

    def get_possible_moves(self, cell):
        '''Returns a list of the valid moves for a cell.'''
        possible_moves = [num for num in range(1, 10)]

        # verif de la ligne
        for col in range(9):
            if self.board[cell.row][col].value in possible_moves:
                possible_moves.remove(self.board[cell.row][col].value)

        # verif de la colonne
        for row in range(9):
            if self.board[row][cell.col].value in possible_moves:
                possible_moves.remove(self.board[row][cell.col].value)

        # verif de la peitite grille
        for row in range(cell.row // 3 * 3, cell.row // 3 * 3 + 3):
            for col in range(cell.col // 3 * 3, cell.col // 3 * 3 + 3):
                if self.board[row][col].value in possible_moves:
                    possible_moves.remove(self.board[row][col].value)

        return possible_moves

    def get_empty_cell(self):
        '''Returns an empty cell. Returns False if all cells are filled in.'''
        for row in range(9):
            for col in range(9):
                if self.board[row][col].value is None:
                    return self.board[row][col]

        return False

    def solve(self):

        cell = self.get_empty_cell()

        if not cell:
            return True

        # tester toute les valeurs possible pour chque case
        for val in range(1, 10):

            if not self.check_move(cell, val):
                continue

            #si le nb est valide la case recoit le nombre
            cell.value = val


            if self.solve():
                return True


            cell.value = None


        return False

    def get_board(self):
        '''Returns a list of values that are in the Sudoku board.'''
        return [[self.board[row][col].value for col in range(9)] for row in range(9)]

    def test_solve(self):
        '''Checks if the current configuration is solvable.'''
        current_board = self.get_board()
        solvable = self.solve()

        for row in range(9):
            for col in range(9):
                self.board[row][col].value = current_board[row][col]

        return solvable

    def reset(self):
        '''Resets the game to its starting state.'''
        for row in self.board:
            for cell in row:
                if cell.editable:
                    cell.value = None


