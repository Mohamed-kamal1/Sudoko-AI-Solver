import tkinter as tk
import GUI.Utilities.Style as S
import GUI.Utilities.Components as Components
import GUI.Utilities.game as G

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.game = G.Game(self)
        self.option_board = tk.StringVar(value=1)  # value = 1 -> AI generated, value = 2 -> Human generated
        self.option_difficulity = tk.StringVar(value=1)  # value = 1 -> Easy, value = 2 -> Intermediate, value = 3 -> Hard
        
        # Main window setup
        self.root.title("Sudoku Solver")
        self.root.geometry("950x550")
        self.root.configure(bg= S.BG_COLOR)

        # Left menu frame
        self.build_menu()

        # Game board frame
        self.build_game()

    def build_menu(self):
        menu_frame = Components.menu(self.root)
        Components.label(menu_frame, "Menu", 16, "center", 20)
        
        # Components.button(menu_frame, "Validate Input", self.validate_input)
        # Components.button(menu_frame, "Exit", self.root.quit)

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

        self.generation_button = Components.button(menu_frame, "Generate Game", self.game.generate_game)

        self.verify_button = Components.button(menu_frame, "Verify board", self.game.verify_board)
        self.verify_button.pack_forget()

        self.board_error = Components.label(menu_frame, "Either the board is unsolvable\n or doesn't have a unique solution",
                                            12, "center", 10, 2)
        self.board_error.pack_forget()

        self.solve_buttton = Components.button(menu_frame, "Solve Sudoku", self.game.solve_sudoku)

        self.step_controls_frame = tk.Frame(menu_frame, bg=S.MENU_BG)
        self.step_controls_frame.pack(pady=0, anchor="center", padx=0)
        Components.button(self.step_controls_frame, "Prev Step", self.game.prev_step, True, 'left')
        Components.button(self.step_controls_frame, "Next Step", self.game.next_step, True, 'right')
        self.step_controls_frame.pack_forget()

    def build_game(self):
        self.game_frame = tk.Frame(self.root, bg=S.BOARD_BG)
        self.game_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=20)
        self.game.generate_game()

    def toggle_board_option(self):
        if (self.option_board.get() == '1'): # AI generated
            self.difficulity_label.pack(anchor="w", pady=0)
            self.radio_diff_frame.pack(pady=5, anchor="w", padx=10)
            self.generation_button.pack(pady=10, fill=tk.X, padx=10)
            self.solve_buttton.pack_forget()
            self.solve_buttton.pack(pady=10, fill=tk.X, padx=10)
            self.verify_button.pack_forget()
            self.board_error.pack_forget()
            self.step_controls_frame.pack_forget()
        else:
            self.difficulity_label.pack_forget()
            self.radio_diff_frame.pack_forget()
            self.solve_buttton.pack_forget()
            self.step_controls_frame.pack_forget()
            self.generation_button.pack_forget()
            self.verify_button.pack(pady=10, fill=tk.X, padx=10)
            self.board_error.pack_forget()
            self.game.generate_game()

    def create_board(self):
        # Creates the Sudoku board on the game frame
        for i in range(9):
            for j in range(9):
                bg_color = S.EMPTY_CELL_BG1 if (i // 3 + j // 3) % 2 == 0 else S.EMPTY_CELL_BG2
                cell = tk.Entry(self.game_frame, width=2, font=(S.FONT_STYLE, 16), justify="center", bg=bg_color, relief=tk.FLAT)
                cell.grid(row=i, column=j, padx=2, pady=2, ipadx=12, ipady=12)
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

    def get_user_input(self):
        self.user_input = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.board[i][j].get().strip()
                if value.isdigit() and 1 <= int(value) <= 9:  # Validate that the input is a number between 1 and 9
                    row.append(int(value))
                else:
                    row.append(0)  # Empty cell, use 0 to represent no value
            self.user_input.append(row)

