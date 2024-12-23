import random

class SudokuGenerator:
    def __init__(self ,empty_cells,box_size = 3):
        self.size = box_size**2
        self.box_size = box_size
        self.empty_cells = empty_cells
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.board_copy = []
        self.generate_board()


    def generate_board(self):
        self.fill_diagonal()
        self.fill_remaining(0,self.box_size)
        self.remove_digits()


    # fill boxes in the diagonal
    def fill_diagonal(self):
        for i in range(0, self.size, self.box_size):
            self.fill_box(i, i)

    # fill box of size box_size * box_size starting from (row, col)
    def fill_box(self, row, col):
        for i in range(self.box_size):
            for j in range(self.box_size):
                while True:
                    num = self.random_generator()
                    if self.is_valid_box(row, col, num):
                        break
                self.board[row + i][col + j] = num

    # fill remaining cells
    def fill_remaining(self,stat_row,start_col):
        # if reached the end of the board
        if stat_row == self.size - 1 and start_col == self.size:
            return True
        # if reached the end of the row
        if start_col == self.size:
            stat_row += 1
            start_col = 0
        # if cell is not empty
        if self.board[stat_row][start_col] != 0:
            return self.fill_remaining(stat_row, start_col + 1)
        # if cell is empty
        for num in range(1, self.size + 1):
            if self.is_valid(stat_row, start_col, num):
                self.board[stat_row][start_col] = num
                if self.fill_remaining(stat_row, start_col + 1):
                    return True
                self.board[stat_row][start_col] = 0

    # generate random numbers in range 1 to size of board
    def random_generator(self):
        return random.randint(1, self.size)

    # check if valid cell
    def is_valid(self, row, col, num):
        return self.is_valid_row(row, num) and self.is_valid_col(col, num) and self.is_valid_box(row, col, num)

    # check if valid row
    def is_valid_row(self,row,num):
        for i in range(self.size):
            if self.board[row][i] == num:
                return False
        return True

    # check if valid column
    def is_valid_col(self,col,num):
        for i in range(self.size):
            if self.board[i][col] == num:
                return False
        return True

    # check if valid box
    def is_valid_box(self,row,col,num):
        start_row = row - row % self.box_size
        start_col = col - col % self.box_size

        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    # remove digits to create puzzle
    def remove_digits(self):
        count = self.empty_cells
        while count != 0:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.board[row][col] != 0:
                backup = self.board[row][col]
                count -= 1
                self.board[row][col] = 0
                num_of_solutions = self.count_solutions(self.board)
                if num_of_solutions != 1:
                    print(num_of_solutions,"Multiple solutions found. Removing digit...")
                    self.board[row][col] = backup
                    count += 1

    # find empty cell
    def find_empty_cell(self,board):
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 0:
                    return i, j

        return None

    # count number of solutions
    def count_solutions(self,board):
        empty_cell = self.find_empty_cell(board)
        if not empty_cell:
            return 1  # Found a valid solution

        row, col = empty_cell
        solution_count = 0

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                board[row][col] = num
                solution_count += self.count_solutions(board)
                board[row][col] = 0  # Backtrack

                # If more than one solution is found, stop further searching
                if solution_count > 1:
                    return solution_count
        return solution_count


def main():
    box_size = 3
    empty_cells = 50
    sudoku = SudokuGenerator(empty_cells,box_size)
    for row in sudoku.board:
        print(row)

if __name__ == "__main__":
    main()