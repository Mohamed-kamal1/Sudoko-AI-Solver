import random
import tkinter as tk
import SudokuGenerator
import Style as S
import Components

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.option_board = tk.StringVar(value=1)  # value = 1 -> AI generated, value = 2 -> Human generated
        self.option_difficulity = tk.StringVar(value=1)  # value = 1 -> Easy, value = 2 -> Intermediate, value = 3 -> Hard
        
        # Main window setup
        self.root.title("Sudoku Solver")
        self.root.geometry("900x510")
        self.root.configure(bg= S.BG_COLOR)

        # Left menu frame
        self.build_menu()

        # Game board frame
        self.build_game()

    def build_menu(self):
        menu_frame = Components.menu(self.root)
        Components.label(menu_frame, "Menu", 16, "center", 20)

        Components.button(menu_frame, "Solve Sudoku", self.solve_sudoku)
        # Components.button(menu_frame, "Validate Input", self.validate_input)
        Components.button(menu_frame, "Exit", self.root.quit)

        Components.label(menu_frame, "Choose Generated Board Mode:", 12, "w", 0)
        radio_frame = tk.Frame(menu_frame, bg=S.MENU_BG)
        radio_frame.pack(pady=5, anchor="w", padx=10)
        Components.radioButton(radio_frame, self.option_board, "AI random board", 1, tk.LEFT, self.toggle_board_option)
        Components.radioButton(radio_frame, self.option_board, "Human made board", 2, tk.RIGHT, self.toggle_board_option)

        self.difficulity_label = Components.label(menu_frame, "Choose Game Difficulity:", 12, "w", 0)
        self.radio_diff_frame = tk.Frame(menu_frame, bg=S.MENU_BG)
        self.radio_diff_frame.pack(pady=5, anchor="w", padx=10)
        Components.radioButton(self.radio_diff_frame, self.option_difficulity, "Easy", 1, tk.LEFT, "")
        Components.radioButton(self.radio_diff_frame, self.option_difficulity, "Intermediate", 2, tk.LEFT, "")
        Components.radioButton(self.radio_diff_frame, self.option_difficulity, "Hard", 3, tk.LEFT, "")

        self.generation_button = Components.button(menu_frame, "Generate Game", self.generate_game)

        self.verify_button = Components.button(menu_frame, "Verify board", self.verify_board)
        self.verify_button.pack_forget()

        self.board_error = Components.label(menu_frame, "Either there ia an invalid input\n or the board is unsolvable\n or doesn't have a unique solution",
                                            12, "center", 10, 2)
        self.board_error.pack_forget()

    def build_game(self):
        self.game_frame = tk.Frame(self.root, bg=S.BOARD_BG)
        self.game_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=20)
        self.generate_game()

    def toggle_board_option(self):
        if (self.option_board.get() == '1'): # AI generated
            self.difficulity_label.pack(anchor="w", pady=0)
            self.radio_diff_frame.pack(pady=5, anchor="w", padx=10)
            self.generation_button.pack(pady=10, fill=tk.X, padx=10)
            self.verify_button.pack_forget()
            self.board_error.pack_forget()
        else:
            self.difficulity_label.pack_forget()
            self.radio_diff_frame.pack_forget()
            self.generation_button.pack_forget()
            self.verify_button.pack(pady=10, fill=tk.X, padx=10)
            self.board_error.pack_forget()
            self.generate_game()

    def generate_game(self):
        # Generate and load a new Sudoku board
        self.board = [[None for _ in range(9)] for _ in range(9)]
        self.create_board()
        
        if (self.option_board.get() == '1'):
            if (self.option_difficulity.get() == '1'):
                num_of_empty_cells = random.randint(35, 45)
                self.board_generator = SudokuGenerator.SudokuGenerator(num_of_empty_cells, 3)
            elif (self.option_difficulity.get() == '2'):
                num_of_empty_cells = random.randint(46, 55)
                self.board_generator = SudokuGenerator.SudokuGenerator(num_of_empty_cells, 3)
            else:
                num_of_empty_cells = random.randint(56, 65)
                self.board_generator = SudokuGenerator.SudokuGenerator(num_of_empty_cells, 3)
            self.load_board(self.board_generator.board)
        else:
            puzzle = [[0 for _ in range(9)] for _ in range(9)]
            self.load_board(puzzle)

    def create_board(self):
        # Creates the Sudoku board on the game frame
        for i in range(9):
            for j in range(9):
                bg_color = S.EMPTY_CELL_BG1 if (i // 3 + j // 3) % 2 == 0 else S.EMPTY_CELL_BG2
                cell = tk.Entry(self.game_frame, width=2, font=(S.FONT_STYLE, 16), justify="center", bg=bg_color, relief=tk.FLAT)
                cell.grid(row=i, column=j, padx=2, pady=2, ipadx=10, ipady=10)
                self.board[i][j] = cell

    def load_board(self, puzzle):
        # Load a new puzzle into the board
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.board[i][j].insert(0, str(puzzle[i][j]))
                    disabled_bg = S.FIXED_NUMBER_BG1 if (i // 3 + j // 3) % 2 == 0 else S.FIXED_NUMBER_BG2
                    self.board[i][j].config(state="disabled", fg="#303036", disabledbackground=disabled_bg)
                else:
                    self.board[i][j].delete(0, tk.END)
                    self.board[i][j].config(state="normal", fg="#000000")

    def solve_sudoku(self):
        # Placeholder for solving Sudoku
        # This function is supposed to get the solved puzzle and view it
        sudoku_solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        self.load_board(sudoku_solution)

    def get_user_input(self):
        user_input = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.board[i][j].get().strip()
                if value.isdigit() and 1 <= int(value) <= 9:  # Validate that the input is a number between 1 and 9
                    row.append(int(value))
                else:
                    row.append(0)  # Empty cell, use 0 to represent no value
            user_input.append(row)
        return user_input

    def verify_board(self):
        user_input = self.get_user_input()
        isValid = True
        if (isValid):
            self.board = [[None for _ in range(9)] for _ in range(9)]
            self.create_board()
            self.load_board(user_input)
        else:
            self.board_error.pack(anchor="center", pady=10)


    def validate_input(self):
        # Validate the Sudoku board input by the user
        for i in range(9):
            for j in range(9):
                value = self.board[i][j].get()
                if value and not value.isdigit():
                    print(f"Invalid input at ({i+1}, {j+1})")
                    return False
                if value and (int(value) < 1 or int(value) > 9):
                    print(f"Invalid value at ({i+1}, {j+1})")
                    return False
        print("All inputs are valid.")
        return True

if __name__ == "__main__":
    root = tk.Tk()
    generator = SudokuGenerator.SudokuGenerator(empty_cells=50)
    SudokuGUI(root)
    root.mainloop()
