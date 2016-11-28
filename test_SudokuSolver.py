hexadoku_expert = [[0,11,0,0,12,0,0,15,0,9,14,0,0,0,3,4],
[0,0,0,0,7,0,0,0,0,1,0,0,11,0,0,0],
[3,8,5,0,0,0,0,0,0,12,0,0,0,0,0,0],
[15,0,12,9,0,0,16,4,0,0,3,0,0,6,0,0],
[1,6,16,0,0,0,9,3,0,0,8,0,0,0,0,0],
[0,3,15,0,0,7,12,0,0,13,0,0,5,2,0,0],
[0,0,0,0,8,0,13,0,0,10,4,1,0,0,0,0],
[2,0,0,0,5,0,0,0,0,0,15,0,0,10,0,0],
[0,5,0,0,0,4,0,9,0,7,10,3,0,1,0,0],
[11,0,9,0,0,0,0,0,8,2,0,0,0,0,0,13],
[0,0,0,0,0,2,0,5,0,0,0,16,0,0,11,0],
[13,12,0,0,6,0,1,8,9,0,0,0,16,0,14,0],
[0,0,0,2,0,0,0,6,0,0,9,10,0,13,16,0],
[0,9,0,8,0,0,5,0,0,0,1,7,15,0,4,0],
[6,0,0,0,0,8,0,1,0,15,0,14,7,5,0,0],
[0,0,4,13,3,0,0,16,0,0,5,0,6,12,0,0]]# This came from the Udacity course on testing and I wanted to use
# graph-traversal to solve this problem efficiently!
import unittest
import random

from SudokuSolver import *
ill_formed = [[5,3,4,6,7,8,9,1,2],
              [6,7,2,1,9,5,3,4,8],
              [1,9,8,3,4,2,5,6,7],
              [8,5,9,7,6,1,4,2,3],
              [4,2,6,8,5,3,7,9],  # <---
              [7,1,3,9,2,4,8,5,6],
              [9,6,1,5,3,7,2,8,4],
              [2,8,7,4,1,9,6,3,5],
              [3,4,5,2,8,6,1,7,9]]

valid = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]
zero_zero_to_five_oneMove = [[0,3,4,6,7,8,9,1,2],
                              [6,7,2,1,9,5,3,4,8],
                              [1,9,8,3,4,2,5,6,7],
                              [8,5,9,7,6,1,4,2,3],
                              [4,2,6,8,5,3,7,9,1],
                              [7,1,3,9,2,4,8,5,6],
                              [9,6,1,5,3,7,2,8,4],
                              [2,8,7,4,1,9,6,3,5],
                              [3,4,5,2,8,6,1,7,9]]

invalid = [[5,3,4,6,7,8,9,1,2],
           [6,7,2,1,9,5,3,4,8],
           [1,9,8,3,8,2,5,6,7],
           [8,5,9,7,6,1,4,2,3],
           [4,2,6,8,5,3,7,9,1],
           [7,1,3,9,2,4,8,5,6],
           [9,6,1,5,3,7,2,8,4],
           [2,8,7,4,1,9,6,3,5],
           [3,4,5,2,8,6,1,7,9]]

easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]
test1_easy = [[1,0,4,0,0,0,3,0,0],
            [0,0,3,0,5,7,0,0,1],
            [0,5,0,0,0,0,0,0,4],
            [0,0,5,0,4,0,6,0,9],
            [7,0,0,8,0,1,0,0,3],
            [4,0,1,0,9,0,2,0,0],
            [8,0,0,0,0,0,0,5,0],
            [9,0,0,6,3,0,1,0,0],
            [0,0,6,0,0,0,9,0,7]]
test1_easy_solution = [[1, 7, 4, 9, 2, 8, 3, 6, 5],
                    [6, 9, 3, 4, 5, 7, 8, 2, 1],
                    [2, 5, 8, 3, 1, 6, 7, 9, 4],
                    [3, 8, 5, 7, 4, 2, 6, 1, 9],
                    [7, 2, 9, 8, 6, 1, 5, 4, 3],
                    [4, 6, 1, 5, 9, 3, 2, 7, 8],
                    [8, 3, 2, 1, 7, 9, 4, 5, 6],
                    [9, 4, 7, 6, 3, 5, 1, 8, 2],
                    [5, 1, 6, 2, 8, 4, 9, 3, 7]]

really_hard = [
            [0,1,0,0,0,8,0,0,9],
            [0,0,4,0,0,0,0,6,0],
            [9,0,6,0,7,0,0,0,0],
            [1,0,2,4,6,9,0,0,8],
            [0,0,0,8,0,5,0,0,0],
            [5,0,0,7,1,3,6,0,2],
            [0,0,0,0,8,0,1,0,7],
            [0,2,0,0,0,0,5,0,0],
            [4,0,0,1,0,0,0,2,0]]

hexadoku_expert = [[0,11,0,0,12,0,0,15,0,9,14,0,0,0,3,4],
                    [0,0,0,0,7,0,0,0,0,1,0,0,11,0,0,0],
                    [3,8,5,0,0,0,0,0,0,12,0,0,0,0,0,0],
                    [15,0,12,9,0,0,16,4,0,0,3,0,0,6,0,0],
                    [1,6,16,0,0,0,9,3,0,0,8,0,0,0,0,0],
                    [0,3,15,0,0,7,12,0,0,13,0,0,5,2,0,0],
                    [0,0,0,0,8,0,13,0,0,10,4,1,0,0,0,0],
                    [2,0,0,0,5,0,0,0,0,0,15,0,0,10,0,0],
                    [0,5,0,0,0,4,0,9,0,7,10,3,0,1,0,0],
                    [11,0,9,0,0,0,0,0,8,2,0,0,0,0,0,13],
                    [0,0,0,0,0,2,0,5,0,0,0,16,0,0,11,0],
                    [13,12,0,0,6,0,1,8,9,0,0,0,16,0,14,0],
                    [0,0,0,2,0,0,0,6,0,0,9,10,0,13,16,0],
                    [0,9,0,8,0,0,5,0,0,0,1,7,15,0,4,0],
                    [6,0,0,0,0,8,0,1,0,15,0,14,7,5,0,0],
                    [0,0,4,13,3,0,0,16,0,0,5,0,6,12,0,0]]


class test_SudokuGrid(unittest.TestCase):

    def test_initializer(self):
        try:
            SudokuGrid(initial_grid = ill_formed)
        except IllFormedGridException:
            self.assertTrue(True, msg="construction did not fail when given malformed grid")

        # should pass without trouble
        testgrid1 = SudokuGrid(initial_grid = valid)

        try:
            SudokuGrid(initial_grid = invalid)
        except InvalidGridException:
            self.assertTrue(True, msg="did not catch invalid grid")

        grid_easy = SudokuGrid(initial_grid = easy)
        grid_hard = SudokuGrid(initial_grid = hard)

        #make several big, empty grids
        for i in range(10):
            big_grid = SudokuGrid(grid_size = i * 30 + 1)

    def test_check_invalid_entry_number(self):
        grid1 = SudokuGrid(initial_grid = None)
        self.assertTrue(grid1.check_invalid_entry_number(-10))
        self.assertTrue(grid1.check_invalid_entry_number(-1))
        for i in range(10):
            self.assertFalse(grid1.check_invalid_entry_number(i))
        self.assertTrue(grid1.check_invalid_entry_number(10))
        self.assertTrue(grid1.check_invalid_entry_number(100))

    def test_toString(self):
        grid1 = SudokuGrid(initial_grid = valid)
        a = str(grid1)

    def test_equals(self):
        grid1 = SudokuGrid(initial_grid = valid)
        grid2 = SudokuGrid(initial_grid = valid)
        grid_easy = SudokuGrid(initial_grid = easy)

        self.assertTrue(grid1==grid2, msg="equals failed when it should be true")
        self.assertFalse(grid1 == grid_easy, msg="equals failed when it should be false")

    def test_possible_moves(self):
        grid_easy = SudokuGrid(initial_grid = easy)
        easy_possible_moves = grid_easy.find_moves()

    def test_hashing(self):
        grid1 = SudokuGrid(initial_grid = valid)
        grid_easy = SudokuGrid(initial_grid = easy)
        grid_hard = SudokuGrid(initial_grid = hard)

        grid_set = {grid1, grid_easy}

        self.assertTrue(grid1 in grid_set)
        self.assertTrue(grid_hard not in grid_set)

    def test_finds_one_possible_move(self):
        grid1 = SudokuGrid(initial_grid = zero_zero_to_five_oneMove)
        grid1_possible_moves = grid1.find_moves()
        self.assertTrue(len(grid1_possible_moves) == 1, "there is only supposed to be one possible move in this grid")

    def test_is_solved(self):
        grid1 = SudokuGrid(initial_grid = valid)
        self.assertTrue(grid1.is_solved(), "Grid should be identified as solved")
        grid2 = SudokuGrid(initial_grid = hard)
        self.assertFalse(grid2.is_solved(), "Grid should not be identified as solved")


class test_SudokuGridSolver(unittest.TestCase):

    def test_initializer(self):
        grid1 = SudokuGrid(initial_grid = zero_zero_to_five_oneMove)
        grid1_solver = SudokuGridSolver(grid1)
    def test_solved_basic(self):
        grid1 = SudokuGrid(initial_grid = zero_zero_to_five_oneMove)
        grid1_solver = SudokuGridSolver(grid1)
        grid1_solved = grid1_solver.solve()
        grid2 = SudokuGrid(initial_grid = valid)
        self.assertTrue(grid2 == grid1_solved)

    def test_solve_easy(self):
        grid_easy = SudokuGrid(initial_grid = easy)
        # print("easy before: \n")
        # print(str(grid_easy))
        grid_easy_solver = SudokuGridSolver(grid_easy)
        grid_easy_solved = grid_easy_solver.solve()
        # print("easy after: \n")
        # print(str(grid_easy_solved))



    def test_solve_easy_1(self):
        grid_easy = SudokuGrid(initial_grid = test1_easy)
        grid_easy_solution = SudokuGrid(initial_grid = test1_easy_solution)
        self.assertTrue(grid_easy_solution.is_solved())
        # print("test1 before: \n")
        # print(str(grid_easy))
        grid_easy_solver = SudokuGridSolver(grid_easy)
        grid_easy_possibly_solved = grid_easy_solver.solve()
        # print("test1 after: \n")
        # print(str(grid_easy_possibly_solved))
        self.assertTrue(grid_easy_possibly_solved == grid_easy_solution)
        self.assertTrue(grid_easy_possibly_solved.is_solved())

    def test_solve_hard(self):
        grid_hard = SudokuGrid(initial_grid = hard)
        grid1_solver = SudokuGridSolver(grid_hard)
        grid_hard_solved = grid1_solver.solve()
        self.assertTrue(grid_hard_solved.is_solved())

    def test_solve_really_hard(self):
        grid_hard = SudokuGrid(initial_grid = really_hard)
        grid1_solver = SudokuGridSolver(grid_hard)
        grid_hard_solved = grid1_solver.solve()
        self.assertTrue(grid_hard_solved.is_solved())

    def test_hexadoku(self):
        print("Do you want to test solving a hexadoku?  It will take ~1.5 hours. Type 'yes' if so:")
        answer = raw_input()
        if answer == 'yes':
            hexagrid = SudokuGrid(initial_grid = hexadoku_expert, grid_size = 16)
            hex_grid_solver = SudokuGridSolver(hexagrid)
            hex_grid_solution = hex_grid_solver.solve()
            self.assertTrue(hex_grid_solution.is_solved())



if __name__ == '__main__':
    unittest.main()
