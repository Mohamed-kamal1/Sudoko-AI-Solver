import random

class SudokuGenerator:
    def __init__(self, empty_cells, box_size=3):
        self.size = box_size**2
        self.box_size = box_size
        self.empty_cells = empty_cells
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.board_copy = []
        self.removed_digits = []
        self.count = 0
        self.rounds = 1
        self.max_removed = 0
        self.generated_board = []
        if empty_cells > 55:
            self.rounds = 5
        for _ in range(self.rounds):
            self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
            self.generate_board()
            print("Round", _ + 1, ":", self.count)
            if self.count > self.max_removed:
                self.max_removed = self.count
                self.board_copy = self.board
        self.board = self.board_copy

    def generate_board(self):
        self.fill_diagonal(self.board)
        self.fill_remaining(self.board, 0, self.box_size)
        self.removed_digits = []
        self.remove_digits(self.board)

    def fill_diagonal(self, board):
        for i in range(0, self.size, self.box_size):
            self.fill_box(board, i, i)

    def fill_box(self, board, row, col):
        for i in range(self.box_size):
            for j in range(self.box_size):
                while True:
                    num = self.random_generator()
                    if self.is_valid_box(board, row, col, num):
                        break
                board[row + i][col + j] = num

    def fill_remaining(self, board, stat_row, start_col):
        if stat_row == self.size - 1 and start_col == self.size:
            return True
        if start_col == self.size:
            stat_row += 1
            start_col = 0
        if board[stat_row][start_col] != 0:
            return self.fill_remaining(board, stat_row, start_col + 1)
        for num in range(1, self.size + 1):
            if self.is_valid(board, stat_row, start_col, num):
                board[stat_row][start_col] = num
                if self.fill_remaining(board, stat_row, start_col + 1):
                    return True
                board[stat_row][start_col] = 0
        return False

    def random_generator(self):
        return random.randint(1, self.size)

    def is_valid(self, board, row, col, num):
        return self.is_valid_row(board, row, num) and self.is_valid_col(board, col, num) and self.is_valid_box(board, row, col, num)

    def is_valid_row(self, board, row, num):
        for i in range(self.size):
            if board[row][i] == num:
                return False
        return True

    def is_valid_col(self, board, col, num):
        for i in range(self.size):
            if board[i][col] == num:
                return False
        return True

    def is_valid_box(self, board, row, col, num):
        start_row = row - row % self.box_size
        start_col = col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def remove_digits(self, board):
        self.count = 0
        while self.count != self.empty_cells and len(self.removed_digits) != self.box_size**4:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if board[row][col] != 0 and (row, col) not in self.removed_digits:
                self.removed_digits.append((row, col))
                backup = board[row][col]
                self.count += 1
                board[row][col] = 0
                num_of_solutions = self.count_solutions(board)
                if num_of_solutions != 1:
                    print(num_of_solutions, "Multiple solutions found. Removing digit...")
                    board[row][col] = backup
                    self.count -= 1

    def find_empty_cell(self, board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return i, j
        return None

    def count_solutions(self, board):
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return 1  # Found a valid solution

        row, col = empty_cell
        solution_count = 0

        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                solution_count += self.count_solutions(board)
                board[row][col] = 0  # Backtrack
                if solution_count > 1:
                    return solution_count
        return solution_count

def main():
    board = [
        [2, 4, 0, 1, 3, 6, 7, 0, 0],
        [1, 8, 3, 5, 7, 0, 4, 6, 9],
        [7, 5, 0, 0, 4, 9, 1, 0, 2],
        [0, 0, 0, 0, 6, 5, 8, 9, 0],
        [3, 1, 0, 0, 0, 8, 0, 0, 0],
        [0, 9, 8, 4, 1, 7, 2, 0, 3],
        [0, 0, 2, 7, 8, 1, 9, 0, 6],
        [8, 6, 0, 0, 9, 3, 5, 1, 0],
        [9, 0, 0, 6, 0, 4, 3, 0, 8]
    ]
    generator = SudokuGenerator(0)  # Initialize with 0 empty cells
    num_solutions = generator.count_solutions(board)
    print("Number of solutions:", num_solutions)

if __name__ == "__main__":
    main()

