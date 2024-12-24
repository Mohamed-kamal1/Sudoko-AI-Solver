from SudokuGenerator import SudokuGenerator
import random
import tkinter as tk
from CSP import CSP
import GUI.Utilities.Style as S

class Game:

    def __init__(self, gui):
        self.gui = gui
        self.count_step = 0

    def generate_game(self):
        # Generate and load a new Sudoku board
        self.count_step = 0
        self.gui.step_controls_frame.pack_forget()
        self.gui.board = [[None for _ in range(9)] for _ in range(9)]
        self.gui.create_board()
        
        if (self.gui.option_board.get() == '1'):
            if (self.gui.option_difficulity.get() == '1'):
                num_of_empty_cells = random.randint(35, 45)
                self.board_generator = SudokuGenerator(num_of_empty_cells, 3)
            elif (self.gui.option_difficulity.get() == '2'):
                num_of_empty_cells = random.randint(46, 55)
                self.board_generator = SudokuGenerator(num_of_empty_cells, 3)
            else:
                num_of_empty_cells = random.randint(56, 65)
                self.board_generator = SudokuGenerator(num_of_empty_cells, 3)
            self.gui.load_board(self.board_generator.board)
            self.gui.solve_buttton.pack(pady=10, fill=tk.X, padx=10)
        else:
            puzzle = [[0 for _ in range(9)] for _ in range(9)]
            self.gui.load_board(puzzle)

    def solve_sudoku(self):
        if self.gui.option_board.get() == '1':
            self.csp = CSP(self.board_generator.board)
        else:
            self.csp = CSP(self.gui.user_input)
            
        self.steps = self.csp.steps
        self.gui.solve_buttton.pack_forget()
        self.gui.step_controls_frame.pack(pady=10, padx=10, fill=tk.X)

    def prev_step(self):
        variable, _ = self.csp.steps[self.count_step - 1]
        row = variable // 9
        coln = variable % 9
        self.gui.board[row][coln].config(state="normal", fg="#000000")
        self.gui.board[row][coln].delete(0, tk.END)

        self.count_step -= 1
        if (self.count_step < 0):
            self.count_step += 1

    def next_step(self):
        self.count_step += 1

        if (len(self.steps) < self.count_step):
            self.count_step -= 1

        variable, value = self.csp.steps[self.count_step - 1]
        row = variable // 9
        coln = variable % 9
        if value != 0:
            self.gui.board[row][coln].insert(0, str(value))
            disabled_bg = S.FIXED_NUMBER_BG1 if (row // 3 + coln // 3) % 2 == 0 else S.FIXED_NUMBER_BG2
            self.gui.board[row][coln].config(state="disabled", fg="#303036", disabledbackground=disabled_bg)
        else:
            self.gui.board[row][coln].delete(0, tk.END)
            self.gui.board[row][coln].config(state="normal", fg="#000000")

    def verify_board(self):                                                # Needs to be configured
        self.count_step = 0
        self.gui.step_controls_frame.pack_forget()
        self.gui.solve_buttton.pack(pady=10, fill=tk.X, padx=10)
        self.gui.get_user_input()

        num_of_sol = SudokuGenerator(0).count_solutions(self.gui.user_input)
        isValid = True if num_of_sol == 1 else False
        if (isValid):
            self.gui.board = [[None for _ in range(9)] for _ in range(9)]
            self.gui.create_board()
            self.gui.load_board(self.gui.user_input)
            self.gui.board_error.pack_forget()
        else:
            self.gui.board_error.pack(anchor="center", pady=10)
        