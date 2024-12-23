from SudokuGenerator import SudokuGenerator
import random
import tkinter as tk
from CSP import CSP

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
                self.gui.board_generator = SudokuGenerator(num_of_empty_cells, 3)
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
            
        self.steps = []
        for step in self.csp.steps:
            board_1d = str(step)
            board_1d = board_1d.zfill(81)
            board_1d = list(map(int, board_1d))
            board_2d = [board_1d[i:i + 9] for i in range(0, 81, 9)]
            self.steps.append(board_2d)
        self.gui.solve_buttton.pack_forget()
        self.gui.step_controls_frame.pack(pady=10, padx=10, fill=tk.X)

    def prev_step(self):
        self.gui.board = [[None for _ in range(9)] for _ in range(9)]
        self.gui.create_board()
        self.gui.load_board(self.steps[self.count_step])
        self.count_step -= 1
        if (self.count_step < 0):
            self.count_step += 1

    def next_step(self):
        self.count_step += 1

        if (len(self.steps) <= self.count_step):
            self.count_step -= 1

        self.gui.board = [[None for _ in range(9)] for _ in range(9)]
        self.gui.create_board()
        self.gui.load_board(self.steps[self.count_step])
    
    def verify_board(self):                                                # Needs to be configured
        self.count_step = 0
        self.gui.step_controls_frame.pack_forget()
        self.gui.solve_buttton.pack(pady=10, fill=tk.X, padx=10)
        self.gui.get_user_input()
        isValid = True
        if (isValid):
            self.gui.board = [[None for _ in range(9)] for _ in range(9)]
            self.gui.create_board()
            self.gui.load_board(self.gui.user_input)
        else:
            self.gui.board_error.pack(anchor="center", pady=10)
        