"""
Solves a sudoku puzzle received in the form of a list of string.
Each string represents a box. Zeros are empty positions.

Example:
 4 7 9 | 0 1 2 | 0 0 0
 0 3 0 | 6 7 0 | 0 1 0
 1 0 2 | 9 0 0 | 7 0 4
-------+-------+-------
 0 0 0 | 0 4 0 | 5 6 8
 6 8 0 | 0 0 0 | 0 0 2
 2 0 0 | 8 6 3 | 0 9 0
-------+-------+-------
 3 4 0 | 0 8 0 | 9 0 0
 0 2 0 | 4 0 0 | 8 0 0
 8 0 1 | 5 2 0 | 4 0 0

A sudoku will be represented:
s_0 = ['479030102', '012670900', '000010704',
       '000680200', '040000863', '568002090',
       '340020801', '080400520', '900800400']

which will be transformed into a dictionary:
sudoku = {'A1': '4', 'A2': '7', ...}

"""
from itertools import combinations


# test problem
s_0 = [
    '479030102', '012670900', '000010704',
    '000680200', '040000863', '568002090',
    '340020801', '080400520', '900800400'
]

s_1 = [
    '003079000', '000035016', '609008070',
    '004000000', '000100007', '005800130',
    '860005900', '000008070', '000200000'
]

test_row = {
    'A1': '4', 'A2': '7', 'A3': '9', 'A4': '3568', 'A5': '1',
    'A6': '2', 'A7': '56', 'A8': '56', 'A9': '568'
}


# Some global variables needed by many methods
rows = 'ABCDEFGHI'
cols = '123456789'

#######################################################################
# methods to represent the sudoku
#######################################################################


def list_to_sudoku(list_representation):
    """
    Reorder the strings so there position corresponds to the grid and
    put them in a dictionary. Replaces all 0 by '123456789'
    :param list_representation: a list of lists representing the sudoku
    grid by boxes
    :return sudoku: a dictionary representing a sudoku puzzle
    """

    digits, sudoku = [], {}

    # reorder list
    for bi in range(3):
        for i in range(3):
            for bj in range(3):
                for j in range(3):
                    digits.append(list_representation[3 * bi + bj][3 * i + j])

    # write dictionary
    for i in range(9):
        for j in range(9):
            cell = rows[i] + cols[j]
            cell_value = digits[9 * i + j]
            if cell_value == '0':
                sudoku[cell] = '123456789'
            else:
                sudoku[cell] = cell_value
    return sudoku


def print_sudoku(sudoku):
    """
    method to produce a nice printout of the problem
    :param sudoku: a dictionary
    """
    cells = [r + c for r in rows for c in cols]
    width = 1 + max(len(sudoku[cell]) for cell in cells)
    h_sep = '+'.join(['-' * ((1 + width) * 3)] * 3)
    for r in rows:
        print(' ' + ' '.join(sudoku[r + c].center(width) + ('|' if c in '36'
                                                            else '') for c in cols))
        if r in 'CF':
            print(h_sep)


#######################################################################
# methods to get cells grouped in rows, columns or boxes
########################################################################


def get_row(cell):
    """
    :param cell: a cell id
    :return: list of cells in the same row
    """
    return [cell[0] + c for c in cols]


def get_col(cell):
    """
    :param cell: a cell id
    :return: list of cells in the same column
    """
    return [r + cell[1] for r in rows]


def get_box(cell):
    """
    :param cell: a cell id
    :return: list of cells in the same box
    """
    boxes = ['ABC', 'DEF', 'GHI', '123', '456', '789']
    rows = ''
    cols = ''
    for rc in boxes:
        if cell[0] in rc:
            rows = rc
        elif cell[1] in rc:
            cols = rc
    box = [r + c for r in rows for c in cols]
    return box


def get_groups():
    """returns the list of all rows, columns and boxes"""
    all_rows = [[r + c for c in cols] for r in rows]
    all_cols = [[r + c for r in rows] for c in cols]
    all_boxes = [[r + c for r in 'ABC' for c in '123']]\
        + [[r + c for r in 'DEF' for c in '123']]\
        + [[r + c for r in 'GHI' for c in '123']]\
        + [[r + c for r in 'ABC' for c in '456']]\
        + [[r + c for r in 'DEF' for c in '456']]\
        + [[r + c for r in 'GHI' for c in '456']]\
        + [[r + c for r in 'ABC' for c in '789']]\
        + [[r + c for r in 'DEF' for c in '789']]\
        + [[r + c for r in 'GHI' for c in '789']]
    return all_rows, all_cols, all_boxes


#######################################################################
# Other methods to modify cells and follow progression
#######################################################################


def remove_digits(string_1, string_2):
    """
    method to remove characters in string2 form string1
    :param string_1, string_2:
    :return: string_1 minus string_2
    """
    modified_string_1 = ''
    for d in string_1:
        if d not in string_2:
            modified_string_1 += d
    return modified_string_1


def union(strings):
    new_string = strings[0]
    for i in range(1, len(strings)):
        for d in strings[i]:
            if d not in new_string:
                new_string += d
    return new_string


def get_subgroups(group_1, group_2):
    """
    From two lists of cells, finds the intersection and the two comple-
    ments
    :param group_1, group_2: the two lists
    :return intersection, comp_1, comp_2: the three subgroups
    """
    intersection, comp_1, comp_2 = [], [], []
    for c in group_1:
        if c in group_2:
            intersection.append(c)
        else:
            comp_1.append(c)
    for c in group_2:
        if c not in intersection:
            comp_2.append(c)
    return intersection, comp_1, comp_2


def progression(sudoku):
    """
    Sums the length of all string in the sudoku cells. A completely
    blank sudoku will have 9*9*9 = 729 possible digits, a completed
    sudoku will have 9*9 = 81 digits. Progress is made
    when digits are removed from the possibilities.
    :param sudoku: the sudoku dictionary
    :return: the number of cells with a single digit value
    """
    state = 0
    for v in sudoku.values():
        state += len(v)
    return state


def validate(sudoku):
    """
    A sudoku is invalid if all digits have been removed form the possible
    values (empty cell). A completed sudoku must have a singl occuence
    of all digits in each row, column and box"
    :param sudoku: a sudoku dictionary
    :return bool: True if valid
    """
    for v in sudoku.values():
        if len(v) < 1:
            return False
    if progression(sudoku) == 81:
        groups = [[r + c for r in 'ABCDEFGHI'] for c in '123456789'] + \
         [[r + c for c in '123456789'] for r in 'ABCDEFGHI'] + \
         [[r+c for r in 'ABC' for c in '123']] + \
         [[r+c for r in 'DEF' for c in '123']] + \
         [[r+c for r in 'GHI' for c in '123']] + \
         [[r+c for r in 'ABC' for c in '456']] + \
         [[r+c for r in 'DEF' for c in '456']] + \
         [[r+c for r in 'GHI' for c in '456']] + \
         [[r+c for r in 'ABC' for c in '789']] + \
         [[r+c for r in 'DEF' for c in '789']] + \
         [[r+c for r in 'GHI' for c in '789']]
        for group in groups:
            digits = []
            for cell in group:
                digits.append(sudoku[cell])
            if sorted(digits) != [str(i) for i in range(1, 10)]:
                return False
    return True


#######################################################################
# Logical test 1
#######################################################################
def logic_1(sudoku):
    """
    checks all the cells in the grid. If unassigned, check all the
    dependent cells and removes assigned values from the possibilities
    :param sudoku:
    """
    for cell, values in sudoku.items():
        if len(sudoku[cell]) > 1:
            dependencies = list(set(get_row(cell)) | set(get_col(cell)) |
                                set(get_box(cell)))
            dependencies.remove(cell)
            assigned_values = []
            for pos in dependencies:
                if len(sudoku[pos]) == 1:
                    assigned_values.append(sudoku[pos])
            # remove them from possibles
            for assigned in assigned_values:
                sudoku[cell] = remove_digits(sudoku[cell], assigned)
                if len(sudoku[cell]) == 0:
                    print('Logic test 1 went wrong {} removed {}'.format(
                        cell, assigned))


#######################################################################
# Logical test 2
#######################################################################
def logic_2(sudoku):
    """
    checks all the cells in the dictionary for unasigned cells. If a
    possible digit is not found in a dependent row, column or box, it
    is assigned to the cell
    :param sudoku: dict
    """
    for cell, values in sudoku.items():
        if len(sudoku[cell]) > 1:
            col_values, row_values, box_values = '', '', ''
            col = get_col(cell)
            col.remove(cell)
            for dep_cell in col:
                col_values += sudoku[dep_cell]
            row = get_row(cell)
            row.remove(cell)
            for dep_cell in row:
                row_values += sudoku[dep_cell]
            box = get_box(cell)
            box.remove(cell)
            for dep_cell in box:
                box_values += sudoku[dep_cell]
            for d in sudoku[cell]:
                if d not in col_values:
                    sudoku[cell] = d
                    print('Logic test 2 found cell {} == {}'.format(
                        cell, sudoku[cell]))
                elif d not in row_values:
                    sudoku[cell] = d
                    print('Logic test 2 found cell {} == {}'.format(
                        cell, sudoku[cell]))
                elif d not in box_values:
                    sudoku[cell] = d
                    print('Logic test 2 found cell {} == {}'.format(
                        cell, sudoku[cell]))


#######################################################################
# Logical test 3
#######################################################################
def logic_3(sudoku):
    """
    checks every row, column and box for cell group for which possible
    values matches the number of cells. These possible values may then
    be removed from all the other cells of the group
    :param sudoku: a sudoku dictionary
    """
    groups = get_groups()[0] + get_groups()[1] + get_groups()[2]
    for group in groups:
        unsolved_cells = []
        permutations = []
        for cell in group:
            if len(sudoku[cell]) > 1:
                unsolved_cells.append(cell)
        for i in range(2, len(unsolved_cells)):
            permutations += list(combinations(unsolved_cells, i))
        for p in permutations:
            digits = []
            for cell in p:
                digits.append(sudoku[cell])
            digits = union(digits)
            if len(digits) == len(p):
                print(p, digits)
                for c in unsolved_cells:
                    if c not in p:
                        sudoku[c] = remove_digits(sudoku[c], digits)
                        print(
                            "Logic test 3 states that {} cannot be in cell {}"
                            .format(digits, c)
                            )


#######################################################################
# Logical test 4
#######################################################################
def logic_4(sudoku):
    """

    """
    for cell in [*sudoku]:
        if len(sudoku[cell]) > 1:
            box = get_box(cell)
            row = get_row(cell)
            col = get_col(cell)
            br_int, br_comp_1, br_comp_2 = get_subgroups(box, row)
            bc_int, bc_comp_1, bc_comp_2 = get_subgroups(box, col)
            br_comp_1_val, br_comp_2_val = '', ''
            bc_comp_1_val, bc_comp_2_val = '', ''
            for cell in br_comp_1:
                br_comp_1_val += sudoku[cell]
            for cell in br_comp_2:
                br_comp_2_val += sudoku[cell]
            for cell in bc_comp_1:
                bc_comp_1_val += sudoku[cell]
            for cell in bc_comp_2:
                bc_comp_2_val += sudoku[cell]
            for cell in br_int:
                print("test 4 to", cell)
                for d in sudoku[cell]:
                    if d not in br_comp_1_val:
                        for c in br_comp_2:
                            if len(sudoku[c]) > 1:
                                print(c, sudoku[c], d)
                                sudoku[c] = remove_digits(sudoku[c], d)
                    elif d not in br_comp_2_val:
                        for c in br_comp_1:
                            if len(sudoku[c]) > 1:
                                print(c, sudoku[c], d)
                                sudoku[c] = remove_digits(sudoku[c], d)
            for cell in bc_int:
                for d in sudoku[cell]:
                    if d not in bc_comp_1_val:
                        for c in bc_comp_2:
                            if len(sudoku[c]) > 1:
                                print(c, sudoku[c], d)
                                sudoku[c] = remove_digits(sudoku[c], d)
                    elif d not in bc_comp_2_val:
                        for c in bc_comp_1:
                            if len(sudoku[c]) > 1:
                                print(c, sudoku[c], d)
                                sudoku[c] = remove_digits(sudoku[c], d)


#######################################################################
# Logic tests application
#######################################################################
def logic_tests(sudoku):
    """
    Applies the three logic tests as long as the sudoku is progressing
    :param sudoku: a sudoku dictionary
    """
    state_i, state = 729, progression(sudoku)
    print("\nSudoku state =", state)
    while state_i > state:
        print("\nSudoku state =", state)
        print("*******************************************************")
        print_sudoku(sudoku)
        print('\ntest 1')
        logic_1(sudoku)
        print_sudoku(sudoku)
        print("sudoku valid", validate(sudoku))
        print("\nTest 2 applied")
        logic_2(sudoku)
        print_sudoku(sudoku)
        print("sudoku valid", validate(sudoku))
        print("\nTest 3 applied")
        logic_3(sudoku)
        print_sudoku(sudoku)
        print("sudoku valid", validate(sudoku))
        print("\nTest 4 applied")
        logic_4(sudoku)
        print_sudoku(sudoku)
        print("sudoku valid", validate(sudoku))
        state_i = state
        state = progression(sudoku)



if __name__ == "__main__":
    sudoku = list_to_sudoku(s_1)
    print_sudoku(sudoku)
    logic_tests(sudoku)
    print("\nTest 4 applied")
    logic_4(sudoku)
    print_sudoku(sudoku)

