import time

from SudokuSolver import *

#DEMO GRIDS:
easy = [[2,9,0,0,0,0,0,7,0],
        [3,0,6,0,0,8,4,0,0],
        [8,0,0,0,4,0,0,0,2],
        [0,2,0,0,3,1,0,0,7],
        [0,0,0,0,8,0,0,0,0],
        [1,0,0,9,5,0,0,6,0],
        [7,0,0,0,9,0,0,0,1],
        [0,0,1,2,0,0,3,0,6],
        [0,3,0,0,0,0,0,5,9]]

really_hard = [[1,0,0,0,0,7,0,9,0],
        [0,3,0,0,2,0,0,0,8],
        [0,0,9,6,0,0,5,0,0],
        [0,0,5,3,0,0,9,0,0],
        [0,1,0,0,8,0,0,0,2],
        [6,0,0,0,0,4,0,0,0],
        [3,0,0,0,0,0,0,1,0],
        [0,4,0,0,0,0,0,0,7],
        [0,0,7,0,0,0,3,0,0]]

hard = [[0,1,0,0,0,8,0,0,9],
                [0,0,4,0,0,0,0,6,0],
                [9,0,6,0,7,0,0,0,0],
                [1,0,2,4,6,9,0,0,8],
                [0,0,0,8,0,5,0,0,0],
                [5,0,0,7,1,3,6,0,2],
                [0,0,0,0,8,0,1,0,7],
                [0,2,0,0,0,0,5,0,0],
                [4,0,0,1,0,0,0,2,0]]


if __name__ == '__main__':
    grid_really_hard = SudokuGrid(initial_grid = really_hard)
    print("Grid to be solved:")
    print(str(grid_really_hard))
    print("...solving....")
    start_time = time.time()
    grid1_solver = SudokuGridSolver(grid_really_hard)
    grid_hard_solved = grid1_solver.solve()
    elapsed_time_s = time.time() - start_time
    print("time Elapsed %f seconds" % elapsed_time_s)

    print("Solution to Puzzle: ")
    print(str(grid_hard_solved))
