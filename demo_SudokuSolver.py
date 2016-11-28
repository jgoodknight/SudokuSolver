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

    print("Try Hexadoku if you dare! (this will take ~1.5 hours to complete)")
    hexagrid = SudokuGrid(initial_grid = hexadoku_expert, grid_size = 16)
    print("Grid to be solved:")
    print(str(hexagrid))
    print("Do you want to solve this? type 'yes' if so:")
    answer = raw_input()
    if answer == 'yes':
        print("...solving....")
        start_time = time.time()
        hex_grid_solver = SudokuGridSolver(hexagrid)
        hex_grid_solution = hex_grid_solver.solve()
        elapsed_time_s = time.time() - start_time
        print("time Elapsed %f seconds" % elapsed_time_s)
        print("Solution to Puzzle: ")
        print(str(hex_grid_solution))
