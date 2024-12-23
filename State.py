import queue
import sys


class State:
    def __init__(self, board, empty_cells, domain):
        self.board = board 
        self.domain = domain
        self.empty_cells = empty_cells    
        
    def assign_new_variable(self, variable, value):
        # update board and empty_cells
        new_board = self.board + value * 10**(81 - variable - 1)
        new_empty_cells = self.empty_cells.copy()
        new_empty_cells.remove(variable)
        return new_board, new_empty_cells
            
    def possible_assign(self):
        # get all possible assignments for all empty cells ordered by least domain using priority queue
        possible_assign =  queue.PriorityQueue()
        for cell in self.empty_cells:
            domain = self.domain[cell]
            count = bin(domain).count('1')
            for bit in range(9):
                if domain & (1 << bit):
                    possible_assign.put((count, cell, bit + 1))
        return possible_assign
        
    
    def update_domain(self, variable):
        # check arc consistency and update domain
        queue = []
        neighbors = self.get_neighbors(variable)
        for neighbor in neighbors:
            queue.append((neighbor, variable))
        while queue:
            neighbor, variable = queue.pop(0)
            if self.revise(neighbor, variable):
                if self.domain[neighbor] == 0:
                    return False
                for n in self.get_neighbors(neighbor):
                    if n != variable:
                        queue.append((n, neighbor))
        return True
       

    def get_neighbors(self, variable):
        # get all neighbors of a variable (same row, same column, same box)
        row = variable // 9
        col = variable % 9
        neighbors = set()                    # to avoid duplicates
        for i in range(9):
            neighbors.add(row * 9 + i)
            neighbors.add(i * 9 + col)
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                neighbors.add((start_row + i) * 9 + start_col + j)
        return neighbors

    def revise(self, neighbor, variable):
        # we need to eliminate the domain of neighbor based on the domain of variable
        # return true in case the neighbor domain is modified  
        revised = False
        domain = self.domain[variable]
        neighbor_domain = self.domain[neighbor]
        for bit in range(9):
            if neighbor_domain & (1 << bit):
                if domain & (1 << bit):
                    self.domain[neighbor] &= ~(1 << bit)
                    revised = True
        return revised

