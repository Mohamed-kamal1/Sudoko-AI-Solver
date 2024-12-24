import copy
import logging
from State import State

# Configure logging
logging.basicConfig(filename='output/solving_process.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class CSP:
    def __init__(self, board):
        self.empty_cells = []  # contains the index of empty cells
        self.init_board = self.to_int(board)
        self.init_domain = [0] * 81
        with open("output/revise_steps.txt", 'w') as file:
            pass 
        with open("output/steps.txt", 'w') as file:
            pass
        self.get_domain(board)
        self.steps = []
        self.init_state = State(self.init_board, self.empty_cells, self.init_domain)
        if not self.check_arc_consistency():
            return
        self.solve(self.init_state)

    def solve(self, state):
        # check if the board is solved
        if len(state.empty_cells) == 0:
            logging.info("Board solved successfully.")
            return True

        possible_assign = state.possible_assign()
        while not possible_assign.empty():
            assign = possible_assign.get()
            logging.info(f"Trying to assign value {assign[2]} to cell ({assign[1] // 9}, {assign[1] % 9})")
            new_board, new_empty_cells, new_domain = state.assign_new_variable(assign[1], assign[2])
            new_state = State(new_board, new_empty_cells, new_domain)
            # check arc consistency and update domain
            consistency = new_state.update_domain(assign[1], self.empty_cells)
            self.steps.append((assign[1], assign[2]))
            self.visualize_step(assign[1], assign[2])
            if not consistency:
                logging.info(f"Assignment of value {assign[2]} to cell ({assign[1] // 9}, {assign[1] % 9}) is inconsistent.")
                continue
            if self.solve(new_state):
                return True

        logging.info("Backtracking...")
        return False

    def to_int(self, board):
        # convert board to int which contains 81 digits
        # get the empty cells
        self.init_board = 0
        for i in range(9):
            for j in range(9):
                self.init_board = self.init_board * 10 + board[i][j]
                if board[i][j] == 0:
                    self.empty_cells.append(i * 9 + j)
        return self.init_board

    def get_domain(self, board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    # then reduce the domain
                    self.reduce_domain(board, i, j)
                else:
                    self.init_domain[i * 9 + j] = 1 << (board[i][j] - 1)

    def reduce_domain(self, board, i, j):
        # reduce the domain of unassigned variable
        # check the row and column and the box
        for num in range(1, 10):
            if self.is_valid_row(board, i, num) and self.is_valid_col(board, j, num) and self.is_valid_box(board, i, j, num):
                self.init_domain[i * 9 + j] |= 1 << (num - 1)

    def is_valid_row(self, board, row, num):
        for i in range(9):
            if board[row][i] == num:
                return False
        return True

    def is_valid_col(self, board, col, num):
        for i in range(9):
            if board[i][col] == num:
                return False
        return True

    def is_valid_box(self, board, row, col, num):
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def check_arc_consistency(self):
        # check arc consistency for all empty cells
        for cell in self.empty_cells:
            consistency = self.init_state.update_domain(cell, self.empty_cells)
            if not consistency:
                return False
        return True

    def visualize_step(self, xi, xj):
        with open('output/steps.txt', 'a') as f:
            f.write(f'Step {len(self.steps)}: Assigning value to cell ({xi // 9}, {xi % 9})\n')
            for i in range(9):
                for j in range(9):
                    f.write(f'Cell ({i}, {j}): Domain {self.init_domain[i * 9 + j]:09b}\n')
            f.write('\n')
        logging.info(f'Step {len(self.steps)}: Assigned value to cell ({xi // 9}, {xi % 9})')
        
        
def main(): 
    board = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    csp = CSP(board)
    