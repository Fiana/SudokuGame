from board import SudokuBoard
import copy


class SudokuGame:
    """
    The Game's Logic
    """
    ROWS = COLUMNS = 9

    def __init__(self, file_name):
        try:
            self.fixed_board = SudokuBoard(file_name)
        except FileNotFoundError:
            exit(1)
        self.player_input = None
        self.missing_elements = None

    def start_game(self):
        """
        Start Game
        """
        self.player_input = copy.deepcopy(self.fixed_board.puzzle)
        counter = 0
        for row in self.player_input:
            for element in row:
                if element == 0:
                    counter += 1
        self.missing_elements = counter

    def insert_number(self, number, row, column):
        """
        inserts a number into a non-fixed cell if the number and cell coordinates are valid.
        :param row: int. range 0 - 8
        :param column: int. range 0 - 8
        :param number: int. range 1 - 9
        :return: True if inserted
        """
        if self.__validate_row_and_col_numbers(row, column) and self.fixed_board.is_cell_empty(row, column):
            if number < 1 or number > 9 and type(number) != int:
                return False
            else:
                if not self.__is_column_valid(number, column):
                    return False
                if not self.__is_row_valid(number, row):
                    return False
                if not self.__is_square_valid(number, row, column):
                    return False
                self.player_input[row][column] = number
                self.missing_elements -= 1
                return True
        return False

    def clear_number(self, row, column):
        """
        Function clear number from a cell from a non-fixed cell 
        :param row: int. range 0 - 8
        :param column: int. range 0 - 8
        :return: True on success
        """
        if self.__validate_row_and_col_numbers(row, column) and self.fixed_board.is_cell_empty(row, column):
            if self.player_input[row][column]:
                self.player_input[row][column] = 0
                self.missing_elements += 1
            return True
        return False

    def is_game_won(self):
        """
        Function returns True if the all missing elements were filled correctly
        :return: True if won otherwise False
        """
        if self.missing_elements == 0:
            return True
        return False

    def __validate_row_and_col_numbers(self, row, column):
        if row < 0 or row >= SudokuGame.ROWS:
            return False
        if column < 0 or column >= SudokuGame.COLUMNS:
            return False
        return True

    def __is_square_valid(self, number, row, column):
        """
        Checks if candidate number is unique in a square of 3X3 cells ,that the selected cell belongs to.
        :param number: int range 1 - 9
        :param row: int. row number of cell
        :param column: int. column number of cell
        :return: True if all the numbers unique
        """

        def calc_start(x): return (x // 3) * 3

        def calc_end(x): return ((x + 3) // 3) * 3

        start_row = calc_start(row)
        end_row = calc_end(row)
        start_col = calc_start(column)
        end_col = calc_end(column)

        square_of_cells = [element for element_list in self.player_input[start_row:end_row]
                 for element in element_list[start_col:end_col]]

        if number in square_of_cells and number != 0:
            return False
        return True

    def __is_row_valid(self, number, row):
        """
        Checks if a candidate number is unique in the row. 
        :param number: int. range 1 - 9
        :param row: int. row number of cell
        :return: True if the number is unique
        """
        row_of_numbers = self.player_input[row]
        if number in row_of_numbers and number != 0:
            return False
        return True

    def __is_column_valid(self, num, column):
        """
        Checks if a candidate number is unique in the column. 
        :param num: int. range 1 - 9
        :param column: int. column number of cell
        :return: True if the number is unique
        """
        col_of_numbers = [row[column] for row in self.player_input]
        if num in col_of_numbers and num != 0:
            return False
        return True
