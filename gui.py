from game import SudokuGame
import tkinter as tk
import tkinter.messagebox as tk_msg
import sys


class SudokuGUI(tk.Frame):
    MARGIN = 20
    SIDE = 50
    WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9
    NUM_FONT = ('Time', '16')

    def __init__(self, master, file_name):
        tk.Frame.__init__(self)
        self.master = master
        self.puzzle = SudokuGame(file_name)
        self.row = 0
        self.column = 0
        self.__initGUI()

    def __initGUI(self):
        self.master.title("Sudoku")
        self.canvas = tk.Canvas(self.master, height=SudokuGUI.HEIGHT, width=SudokuGUI.WIDTH)
        self.canvas.pack()
        button_clear = tk.Button(self.master, text="clear", font=SudokuGUI.NUM_FONT, command=self.__draw_numbers)
        button_clear.pack()
        self.__draw_board_grid()
        self.__draw_numbers()
        self.canvas.bind("<Button-1>", self.__sudoku_cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)

    def __draw_board_grid(self):
        for i in range(10):
            if i % 3:
                color = "grey"
            else:
                color = "blue"
            self.canvas.create_line(SudokuGUI.MARGIN, SudokuGUI.MARGIN + SudokuGUI.SIDE * i,
                                    SudokuGUI.WIDTH - SudokuGUI.MARGIN, SudokuGUI.MARGIN + SudokuGUI.SIDE * i,
                                    fill=color, width=2)
            self.canvas.create_line(SudokuGUI.MARGIN + SudokuGUI.SIDE * i, SudokuGUI.MARGIN,
                                    SudokuGUI.MARGIN + SudokuGUI.SIDE * i, SudokuGUI.HEIGHT - SudokuGUI.MARGIN,
                                    fill=color, width=2)

    def __draw_numbers(self):
        self.canvas.delete("puzzle numbers", "cells", "user numbers")
        self.puzzle.start_game()
        for i in range(9):
            for j in range(9):
                x0, y0, x1, y1 = self.__calc_cell_canvas_coordinates(i, j)
                if self.puzzle.player_input[i][j]:
                    answer = self.puzzle.player_input[i][j]
                    self.canvas.create_rectangle(x0 + 1, y0 + 1, x1 - 1, y1 - 1, width=0, fill="light grey",
                                                 tags="cells")
                else:
                    answer = ""
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=answer, font=SudokuGUI.NUM_FONT,
                                        tags="puzzle numbers")

    def __calc_cell_canvas_coordinates(self, row, column):
        """
        Given the row and the column of the cell returns the rectangle coordinates in the gui
        :param row: int  
        :param column: int
        :return: x0, y0 - the start coordinates. x1, y1 - the finish coordinates
        """
        x0 = SudokuGUI.MARGIN + column * SudokuGUI.SIDE
        y0 = SudokuGUI.MARGIN + row * SudokuGUI.SIDE
        x1 = SudokuGUI.MARGIN + (column + 1) * SudokuGUI.SIDE
        y1 = SudokuGUI.MARGIN + (row + 1) * SudokuGUI.SIDE
        return x0, y0, x1, y1

    def __sudoku_cell_clicked(self, event):
        x = event.x
        y = event.y
        x_limits = (SudokuGUI.MARGIN, SudokuGUI.WIDTH - SudokuGUI.MARGIN)
        y_limits = (SudokuGUI.MARGIN, SudokuGUI.HEIGHT - SudokuGUI.MARGIN)

        if x_limits[0] < x < x_limits[1] and y_limits[0] < y < y_limits[1]:
            self.canvas.focus_set()
        else:
            return

        col = int((x - x_limits[0]) // SudokuGUI.SIDE)
        row = int((y - y_limits[0]) // SudokuGUI.SIDE)

        if row != self.row or col != self.column:
            self.row = row
            self.column = col
            self.__highlight_cell()

    def __highlight_cell(self):
        self.canvas.delete("cursor")
        if self.row != -1:
            self.canvas.create_rectangle(self.__calc_cell_canvas_coordinates(self.row, self.column), outline="red",
                                         width=2,
                                         tags="cursor")

    def __key_pressed(self, event):
        if self.row == -1 or not self.puzzle.fixed_board.is_cell_empty(self.row, self.column):
            return
        tag_name = str(self.row) + " " + str(self.column)

        if event.char.isdigit() and 0 < int(event.char) < 10:
            if int(event.char) != self.puzzle.player_input[self.row][self.column]:
                self.__write_number_in_cell(tag_name, int(event.char))
        elif event.keysym == 'Delete' or event.keysym == 'BackSpace':
            self.__clear_number_in_cell(tag_name)

        if self.puzzle.is_game_won():
            tk_msg.showinfo("Hello winner", "You Won")

    def __clear_number_in_cell(self, tag_name):
        self.canvas.delete(tag_name)
        self.puzzle.clear_number(self.row, self.column)

    def __write_number_in_cell(self, tag_name, number):
        self.__clear_number_in_cell(tag_name)
        x0, y0, x1, y1 = self.__calc_cell_canvas_coordinates(self.row, self.column)
        if self.puzzle.insert_number(number, self.row, self.column):
            color = "black"
        else:
            color = "red"
        self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=number,
                                font=SudokuGUI.NUM_FONT, tags=("user numbers", tag_name), fill=color)
