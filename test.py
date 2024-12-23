import unittest
from CSP import CSP

class TestCSP(unittest.TestCase): 
    def setUp(self):
        self.board = [
            [6, 0, 8, 0, 0, 0, 0, 0, 0],
            [0, 4, 0, 1, 0, 0, 5, 0, 0],
            [0, 0, 1, 0, 0, 6, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 2, 0, 0, 9, 0],
            [0, 3, 0, 4, 0, 0, 7, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 8, 0],
            [3, 8, 0, 0, 0, 4, 0, 2, 0],
            [0, 9, 0, 7, 0, 0, 0, 3, 0]
        ]
        self.csp = CSP(self.board)

    def test_1(self):
        expected = [
                [6, 7, 8, 2, 9, 5, 3, 1, 4],
                [9, 4, 3, 1, 7, 8, 5, 6, 2],
                [2, 5, 1, 3, 4, 6, 9, 7, 8],
                [5, 6, 9, 8, 1, 7, 2, 4, 3],
                [4, 1, 7, 5, 2, 3, 8, 9, 6],
                [8, 3, 2, 4, 6, 9, 7, 5, 1],
                [7, 2, 5, 6, 3, 1, 4, 8, 9],
                [3, 8, 6, 9, 5, 4, 1, 2, 7],
                [1, 9, 4, 7, 8, 2, 6, 3, 5]
            ]
        step = self.csp.steps[len(self.csp.steps) - 1]
        self.assertEqual(step, self.csp.to_int(expected))

if __name__ == '__main__':
    unittest.main()
    
    
