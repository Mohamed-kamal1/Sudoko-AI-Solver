from State import State


class CSP:
    def __init__(self, board):
        self.empty_cells = []  # contains the index of empty cells 
        self.init_board = self.to_int(board)
        self.init_domain = [0] * 81
        self.get_domain(board)
        self.steps = [self.init_board]
        self.init_state = State(self.init_board, self.empty_cells, self.init_domain)
        self.solve(self.init_state)
        # note that we need to check all arcs of all empty cells before solving the board

    def solve(self, state):
        # check if the board is solved
        if len(state.empty_cells) == 0:
            return True

        possible_assign = state.possible_assign()
        while not possible_assign.empty():
            assign = possible_assign.get()
            new_board, new_empty_cells = state.assign_new_variable(assign[1], assign[2])
            new_state = State(new_board, new_empty_cells, state.domain.copy())
            print(new_board)
            # check arc consistency and update domain
            consistency = new_state.update_domain(assign[1])
            self.steps.append(new_board)
            if not consistency:
                continue
            if self.solve(new_state):
                return True

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


board = [
    [7, 0, 0, 0, 4, 0, 0, 0, 9],
    [0, 0, 3, 0, 0, 0, 0, 0, 0],
    [5, 0, 0, 0, 8, 0, 2, 0, 1],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 4, 6, 0, 0, 0, 7, 1, 0],
    [8, 7, 0, 0, 1, 0, 0, 0, 4],
    [0, 3, 0, 4, 7, 5, 1, 0, 0],
    [0, 0, 7, 0, 6, 2, 5, 0, 0],
    [0, 5, 0, 0, 9, 1, 6, 0, 3]
]

csp = CSP(board)
# turn the each step into 2d array
steps = [list(map(int, str(step))) for step in csp.steps]
# print it in readable way
for step in steps:
    for i in range(9):
        print(step[i * 9:i * 9 + 9])
    print()