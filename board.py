class SudokuBoard:
    """"
        loads sudoku puzzle configuration from file
    """

    def __init__(self, file_name):
        self.puzzle = self.load_puzzle(file_name)

    def load_puzzle(self, file_name):
        """
        Function loads a puzzle configuration from a file
        :param file_name: str
        :return: list of lists. size: 9 x 9
        """
        file_id = open(file_name, 'r')
        line_list = file_id.readlines()
        matrix = []
        row_counter = 0

        for line in line_list:
            column_counter = 0
            row = []
            for element in line.split():
                if element.isdigit() and 0 <= int(element) < 10:
                    row.append(int(element))
                    column_counter += 1
            if column_counter != 9:
                raise ValueError("Error: input file cannot create puzzle. Needed 9X9 matrix in the file")
            matrix.append(row)
            row_counter += 1
            if row_counter > 9:
                raise ValueError("Error: input file cannot create puzzle. Needed 9X9 matrix int the file")

        file_id.close()
        return matrix

    def is_cell_empty(self, row, col):
        """
        Function checks if the cell at (row, column) in the puzzle doesn't contain a number
        :param row: int. range 0 - 8.
        :param col: int. range 0 - 8
        :return: True only if the cell is empty.
        """
        return not self.puzzle[row][col]

