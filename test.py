import unittest
from CSP import CSP

class TestCSP(unittest.TestCase): 
    def setUp(self):
        self.board = [
            [0, 0, 0, 2, 0, 0, 0, 0, 8],
            [3, 0, 0, 4, 0, 0, 1, 0, 9],
            [0, 0, 5, 7, 8, 0, 4, 3, 0],
            [0, 3, 0, 0, 0, 2, 8, 0, 0],
            [1, 0, 2, 0, 0, 0, 3, 0, 7],
            [0, 0, 7, 0, 3, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 5],
            [0, 5, 0, 0, 0, 7, 0, 0, 3],
            [7, 0, 3, 0, 9, 0, 0, 4, 6]
        ]
        self.csp = CSP(self.board)

    def test_initial_board(self):
        expected_board = 0
        for row in self.board:
            for num in row:
                expected_board = expected_board * 10 + num
        self.assertEqual(self.csp.init_board, expected_board)
        
    def test_is_valid_row(self):
        self.assertTrue(self.csp.is_valid_row(self.board, 0, 1))
        self.assertFalse(self.csp.is_valid_row(self.board, 0, 2))

    def test_is_valid_box(self):
        self.assertTrue(self.csp.is_valid_box(self.board, 0, 0, 1))
        self.assertFalse(self.csp.is_valid_box(self.board, 0, 0, 3))

    def test_solve(self):
        solved = self.csp.solve(self.csp.init_state)
        # self.assertTrue(solved)
        self.assertEqual(len(self.csp.steps[-1]), 81)
        self.assertNotIn('0', str(self.csp.steps[-1]))

if __name__ == '__main__':
    unittest.main()