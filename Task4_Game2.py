import tkinter as tk
from tkinter import messagebox
import random

class SudokuGUI:
    def _init_(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0]*9 for _ in range(9)]
        self.entries = [[None]*9 for _ in range(9)]
        self.create_widgets()
        self.generate_puzzle()

    def create_widgets(self):
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.master, width=3, font=('Arial', 18), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                self.entries[i][j] = entry

        solve_button = tk.Button(self.master, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=9, column=4, pady=10)

    def generate_puzzle(self):
        self.board = self.generate_full_board()
        self.remove_numbers_from_board()
        self.update_entries()

    def generate_full_board(self):
        board = [[0]*9 for _ in range(9)]
        self.fill_diagonal_boxes(board)
        self.fill_remaining_boxes(board, 0, 3)
        return board

    def fill_diagonal_boxes(self, board):
        for i in range(0, 9, 3):
            self.fill_box(board, i, i)

    def fill_box(self, board, row, col):
        num = 1
        for i in range(3):
            for j in range(3):
                while not self.is_safe(board, row+i, col+j, num):
                    num = random.randint(1, 9)
                board[row+i][col+j] = num

    def is_safe(self, board, row, col, num):
        return self.not_in_row(board, row, num) and self.not_in_col(board, col, num) and self.not_in_box(board, row-row%3, col-col%3, num)

    def not_in_row(self, board, row, num):
        return num not in board[row]

    def not_in_col(self, board, col, num):
        return num not in [board[row][col] for row in range(9)]

    def not_in_box(self, board, box_start_row, box_start_col, num):
        for i in range(3):
            for j in range(3):
                if board[box_start_row+i][box_start_col+j] == num:
                    return False
        return True

    def fill_remaining_boxes(self, board, i, j):
        if j >= 9 and i < 8:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True
        if i < 3:
            if j < 3:
                j = 3
        elif i < 6:
            if j == int(i/3)*3:
                j += 3
        else:
            if j == 6:
                i += 1
                j = 0
                if i >= 9:
                    return True
        for num in range(1, 10):
            if self.is_safe(board, i, j, num):
                board[i][j] = num
                if self.fill_remaining_boxes(board, i, j+1):
                    return True
                board[i][j] = 0
        return False

    def remove_numbers_from_board(self):
        count = 20
        while count != 0:
            cell_id = random.randint(0, 80)
            row = cell_id // 9
            col = cell_id % 9
            if self.board[row][col] != 0:
                count -= 1
                self.board[row][col] = 0

    def update_entries(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.entries[i][j].insert(0, self.board[i][j])
                    self.entries[i][j].config(state='disabled')
                else:
                    self.entries[i][j].config(state='normal')
                    self.entries[i][j].delete(0, tk.END)

    def solve_puzzle(self):
        self.solve_board(self.board)
        self.update_entries()

    def solve_board(self, board):
        empty = self.find_empty_location(board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_board(board):
                    return True
                board[row][col] = 0
        return False

    def find_empty_location(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

if __name__ == "_main_":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()
