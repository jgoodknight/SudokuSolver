# This came from the Udacity course on testing and I wanted to use
# graph-traversal to solve this problem efficiently!

import math
import copy
import random

import numpy as np


class SudokuGrid(object):
    """
    Represents an arbitrary-sized Sudoku Grid for the purposes of storage and solving
    Is not guaranteed to be solveable or to be a valid grid past being the right shape and not having
    items which are invalid numbers
    """
    def __init__(self, grid_size = 9, initial_grid = None):
        assert(grid_size > 0)
        assert(int(math.sqrt(grid_size))**2 == grid_size, "grid size must be a perfect square")

        self.grid_size = grid_size
        self.small_box_size = int(math.sqrt(grid_size))
        self.grid_shape = (self.grid_size, self.grid_size)

        self.my_grid = np.zeros(self.grid_shape, dtype=np.int)

        if initial_grid is not None:
            self.test_validity_and_initialize_grid(grid_input = initial_grid)
        else:
            #then we want a grid of zeros to be filled in later and there's no point in checking if we have a valid grid
            pass

    def test_validity_and_initialize_grid(self, grid_input):
        """
        Takes the input inital grid and fills out the internal data structure
        raises an error for repeat indeces

        TIME COMPLEXITY: O(self.grid_size^2)
        SPACE COMPLEXITY: O(self.grid_size)
        """
        initial_grid = grid_input
        if len(initial_grid) != self.grid_size:
            raise IllFormedGridException("wrong number of rows" )

        #set up search dictionaries
        col_index_to_found_numbers_set = {}
        internal_box_indeces_to_found_numbers_set = {}

        for row_i in range(self.grid_size):
            #new row, initialize dictionary of found numbers
            found_numbers_in_row = set()

            #get row data, check size
            row_data = initial_grid[row_i]

            if len(row_data) != self.grid_size:
                raise IllFormedGridException("wrong row number in row %i" % row_i)

            #iterate through columns
            for col_i in range(self.grid_size):
                try:
                    col_index_to_found_numbers_set[col_i]
                except:
                    col_index_to_found_numbers_set[col_i] = set()

                #find the internal box coordinates
                int_row_i, int_col_i = self.get_internal_box_coordinate(row_i, col_i)
                #see if there's a set already, if not make one
                try:
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]
                except:
                    internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)] = set()
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]

                # finally, get the relevant data
                dat = row_data[col_i]
                #check if the data is a valid number
                if self.check_invalid_entry_number(dat):
                    raise IllFormedGridException("invalid number %i for grid size %i" % (dat, self.grid_size))

                # see if we've already found the data in a relevant location
                if dat != 0:
                    if dat in found_numbers_in_row:
                        raise InvalidGridException("repeat numbers found in row " + str(row_i))
                    if dat in col_index_to_found_numbers_set[col_i]:
                        raise InvalidGridException("repeat numbers found in column " + str(col_i))
                    if dat in internal_set:
                        raise InvalidGridException("repeat numbers found in internal boc " + str(int_row_i) +","+ str(int_col_i))
                    else:
                        found_numbers_in_row.add(dat)
                        col_index_to_found_numbers_set[col_i].add(dat)
                        internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)].add(dat)

                #it's finally safe to add the number to the grid!
                self.my_grid[row_i, col_i] = dat
    def check_validity(self,):
        """
        Checks the validity of the grid, possibly after a move or for a sanity check

        TIME COMPLEXITY: O(self.grid_size^2)
        SPACE COMPLEXITY: O(self.grid_size)
        """
        #set up search dictionaries
        col_index_to_found_numbers_set = {}
        internal_box_indeces_to_found_numbers_set = {}

        for row_i in range(self.grid_size):
            #new row, initialize dictionary of found numbers
            found_numbers_in_row = set()

            #get row data, check size
            row_data = self.my_grid[row_i]

            #iterate through columns
            for col_i in range(self.grid_size):
                try:
                    col_index_to_found_numbers_set[col_i]
                except:
                    col_index_to_found_numbers_set[col_i] = set()

                #find the internal box coordinates
                int_row_i, int_col_i = self.get_internal_box_coordinate(row_i, col_i)
                #see if there's a set already, if not make one
                try:
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]
                except:
                    internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)] = set()
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]

                # finally, get the relevant data
                dat = row_data[col_i]
                #check if the data is a valid number
                if self.check_invalid_entry_number(dat):
                    raise IllFormedGridException("invalid number %i for grid size %i" % (dat, self.grid_size))

                # see if we've already found the data in a relevant location
                if dat != 0:
                    if dat in found_numbers_in_row:
                        raise InvalidGridException("repeat numbers found in row " + str(row_i))
                    if dat in col_index_to_found_numbers_set[col_i]:
                        raise InvalidGridException("repeat numbers found in column " + str(col_i))
                    if dat in internal_set:
                        raise InvalidGridException("repeat numbers found in internal boc " + str(int_row_i) +","+ str(int_col_i))
                    else:
                        found_numbers_in_row.add(dat)
                        col_index_to_found_numbers_set[col_i].add(dat)
                        internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)].add(dat)

                #it's finally safe to add the number to the grid!
                return True

    def check_invalid_entry_number(self, entry_number):
        "Returns true if the input number belongs in the grid"
        return entry_number > self.grid_size or entry_number < 0

    def find_moves(self):
        """
        Returns a list of tuples ((row_i, col_i), possible_number) for all seemingly valid moves
        should only be used at the beginning, because it is inefficient if you already know the
        subset of possible moves

        SPACE COMPLEXITY: O(self.grid_size^3) worst case
        TIME COMPLEXITY: O(self.grid_size^2)

        1) finds all filled in indeces
        2) for indeces not filled in creates a dictionary indexed by (row_i, col_i), of a set of possible moves
        3) goes through by row and removes bad moves in set
        4) goes through by column and removes bad moves in set
        5) goes through the internal box and removes all bad moves in the set
        """
        possible_moves = {}
        defined_indeces = set([])
        for (row_i, col_i), dat in np.ndenumerate(self.my_grid):
            if dat != 0:
                defined_indeces.add((row_i, col_i))
            else:
                possible_moves[(row_i, col_i)] = set(range(1,self.grid_size + 1))

        #go through the defined indeces and update the possible moves based on the included data
        #surround in try to catch an error

        for (row_i, col_i) in defined_indeces:
            dat = self[row_i, col_i]

            #take the data in every defined index and remove the data from all items in its row and column
            for other_index in range(self.grid_size):
                if (row_i, other_index) not in defined_indeces:
                    possible_moves[(row_i, other_index)].discard(dat)
                if (other_index, col_i) not in defined_indeces:
                    possible_moves[(other_index, col_i)].discard(dat)

            box_row_indeces, box_col_indeces = self.get_internal_box_indeces(row_i, col_i)

            for row_i in box_row_indeces:
                for col_i in box_col_indeces:
                    if (row_i, col_i) not in defined_indeces:
                        possible_moves[(row_i, col_i)].discard(dat)
        return possible_moves

    def is_solved(self):
        """
        Returns true if this is a solved sudoku, False if not

        TIME COMPLEXITY: O(self.grid_size^2)
        SPACE COMPLEXITY: O(self.grid_size)
        """
        #set up search dictionaries
        col_index_to_found_numbers_set = {}
        internal_box_indeces_to_found_numbers_set = {}

        for row_i in range(self.grid_size):
            #new row, initialize dictionary of found numbers
            found_numbers_in_row = set()

            #get row data, check size
            row_data = self.my_grid[row_i,:]

            #iterate through columns
            for col_i in range(self.grid_size):
                try:
                    col_index_to_found_numbers_set[col_i]
                except:
                    col_index_to_found_numbers_set[col_i] = set()

                #find the internal box coordinates
                int_row_i, int_col_i = self.get_internal_box_coordinate(row_i, col_i)
                #see if there's a set already, if not make one
                try:
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]
                except:
                    internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)] = set()
                    internal_set = internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)]

                # finally, get the relevant data
                dat = row_data[col_i]
                if dat == 0:
                    return False
                # check to make sure the number is valid
                assert(not self.check_invalid_entry_number(dat))
                # see if we've already found the data in a relevant location
                if dat in found_numbers_in_row:
                    raise InvalidGridException("repeat numbers found in row " + str(row_i))
                if dat in col_index_to_found_numbers_set[col_i]:
                    raise InvalidGridException("repeat numbers found in column " + str(col_i))
                if dat in internal_set:
                    raise InvalidGridException("repeat numbers found in internal boc " + str(int_row_i) +","+ str(int_col_i))
                else:
                    found_numbers_in_row.add(dat)
                    col_index_to_found_numbers_set[col_i].add(dat)
                    internal_box_indeces_to_found_numbers_set[(int_row_i, int_col_i)].add(dat)

        return True

    def get_internal_box_indeces(self, row_i, col_i):
        """
        function to return the other indeces which are in the same box as the given index
        """
        internal_row_index, internal_col_index = self.get_internal_box_coordinate(row_i, col_i)

        row_indeces = internal_row_index * self.small_box_size +  np.array(range(self.small_box_size))
        col_indeces = internal_col_index * self.small_box_size +  np.array(range(self.small_box_size))

        return row_indeces, col_indeces
    def get_internal_box_coordinate(self, row_i, col_i):
        """
        function to return the internal box coordinate
        """
        internal_row_index = math.ceil(row_i / self.small_box_size)
        internal_col_index = math.ceil(col_i / self.small_box_size)

        return internal_row_index, internal_col_index

    def make_move(self, row_i, col_i, new_number, ensure_safe_addition=True):
        output = copy.deepcopy(self)
        assert(not output.check_invalid_entry_number(new_number) )
        if output[row_i, col_i] != 0:
            raise InvalidMoveException("Space must be empty to make a move")
        output.my_grid[row_i, col_i] = new_number
        if ensure_safe_addition:
            assert(output.check_validity())
        return output

    #OPERATOR OVERLOADING
    def __getitem__(self, row_col_tuple):
        row_i,col_i = row_col_tuple
        return self.my_grid[row_i,col_i]

    def __eq__(self, otherSudokuGrid):
        for (i, j), item in np.ndenumerate(self.my_grid):
            if otherSudokuGrid[i,j] != item:
                return False
        return True

    def __str__(self):
        output = ""
        for row_i in range(self.grid_size):

            for col_j in range(self.grid_size):
                dat = self[row_i, col_j]
                if dat > self.grid_size or dat < 0:
                    raise IllFormedGridException("invalid number %i for grid size %i" %(dat, self.grid_size))
                output = output + " " + str(dat)
            output = output + """\n"""
        return output

    def __hash__(self):
        return hash((str(self)))

class SudokuGridSolver(object):
    """
    An object to contain the logic for solving a SudokuGrid solution
    """
    def __init__(self, SudokuGridInstance):
        self.initial_SudokuGrid = SudokuGridInstance

    def solve(self):
        possible_moves_index_to_set = self.initial_SudokuGrid.find_moves()
        working_copy_of_initial_SudokuGrid = copy.deepcopy(self.initial_SudokuGrid)
        working_copy_of_initial_SudokuGrid = self.__make_trivial_moves__(working_copy_of_initial_SudokuGrid, possible_moves_index_to_set)
        #find a grid point with the minimum number of possible moveset

        return working_copy_of_initial_SudokuGrid

    def __make_trivial_moves__(self, working_copy_of_initial_SudokuGrid, possible_moves_index_to_set):
        # Go through and pick low-hanging fruit until none exists
        # Find squares for which there is only one possible moveset
        found_easy_move = True
        moves_made = 0
        while found_easy_move:
            found_easy_move = False
            for (row_i, col_i) in possible_moves_index_to_set.keys():
                possile_move_set = possible_moves_index_to_set[row_i, col_i]
                #size zero moveset implies impossible solution
                if len(possile_move_set) == 0:
                    raise UnsolveableSudokuGrid("space %i, %i has no possible moves!" % (row_i, col_i))
                # one possible move means we can do something!
                if len(possile_move_set) == 1:
                    new_number = possile_move_set.pop()
                    working_copy_of_initial_SudokuGrid = working_copy_of_initial_SudokuGrid.make_move(row_i, col_i, new_number, ensure_safe_addition=False)
                    
                    moves_made = moves_made + 1
                    del possible_moves_index_to_set[(row_i, col_i)]
                    # Check row, column and internal box membership
                    for other_row_i, other_col_i in possible_moves_index_to_set.keys():
                        if other_row_i == row_i:
                            possible_moves_index_to_set[(other_row_i, other_col_i)].discard(new_number)
                        if other_col_i == col_i:
                            possible_moves_index_to_set[(other_row_i, other_col_i)].discard(new_number)

                    # Check internal box membership
                    internal_rows, internal_columns = working_copy_of_initial_SudokuGrid.get_internal_box_indeces(row_i, col_i)
                    for other_row_i in internal_rows:
                        for other_col_i in internal_columns:
                            #see if this box has the offensive number as a possibility, remove if so
                            try:
                                possible_moves_index_to_set[(other_row_i, other_col_i)].discard(new_number)
                            except KeyError:
                                pass
                    #mark that we found an easy move
                    found_easy_move = True
                    break #restart the loop now that the possible moves are updated
        print("SudokuSolver made %i trivial moves" % moves_made)
        return working_copy_of_initial_SudokuGrid





class InvalidGridException(Exception):
    """
    Throws when the SudokuGrid initializer is found to be unsolveable
    """
    def __init__(self, message):
        self.message = message

class InvalidMoveException(Exception):
    """
    Throws when attempting to make and invalid move on a SudokuGrid
    """
    def __init__(self, message):
        self.message = message


class IllFormedGridException(Exception):
    """
    Throws when the SudokuGrid initializer is given an misshapen inital_grid argument
    """
    def __init__(self, message):
        self.message = message


class UnsolveableSudokuGrid(Exception):
    """
    Throws when the SudokuGrid discovers it is unable to be solved
    """
    def __init__(self, message):
        self.message = message