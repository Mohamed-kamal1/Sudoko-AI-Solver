import time
from CSP import CSP
from SudokuGenerator import SudokuGenerator

def measure_runtime(empty_cells):
    generator = SudokuGenerator(empty_cells)
    board = generator.board
    csp_solver = CSP(board)

    start_time = time.time()
    solved = csp_solver.solve(csp_solver.init_state)
    end_time = time.time()

    runtime = end_time - start_time
    return runtime, solved

def main():
    empty_cells_list = [25,26,33,34,35,
                        42,44,45,47,49,
                        50,52,54,55,57]
    results = []

    with open('output/runtime_results.txt', 'w') as f:
        for empty_cells in empty_cells_list:
            runtime, solved = measure_runtime(empty_cells)
            print(f"Empty cells: {empty_cells}, Runtime: {runtime:.4f} seconds, Solved: {solved}")
            results.append((empty_cells, runtime, solved))
            f.write(f"Empty cells: {empty_cells}, Runtime: {runtime:.4f} seconds, Solved: {solved}\n")

if __name__ == "__main__":
    main()