from gui import SudokuGUI
from tkinter import Tk

if __name__ == "__main__":
    path = r"puzzles/"
    file_name = r"puzzle_1"

    root = Tk()
    gui = SudokuGUI(root, path + file_name)
    root.mainloop()
