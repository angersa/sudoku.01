"""
Generates a sudoku problems starting with a rendom grid (solution).
The program will generate a partial sudoku by creating a random list
of digits representing boxes 1,4 and 9 of a sudoku. It will then uses
sudoku_solver.py to solve the sudoku.

Cells will then be removed randomly, checking solvability and validity
after each substration. Different difficulty levels will be obtained
by determinitng the tests to use as such:
- EASY (level = 1): Only logic tests 1 and 2 allowed
- DIFFICULT (level 2): All logic tests allowed, but no branching
- EXPERT (level 3): Branching once is allowed
"""
from random import shuffle
import os
import sudoku_solver as ss


def random_grid_generator():
    """
    Generates a complete grid from random input
    :return: a completed sudoku dictionary
    """
    sudoku_list = ['0' * 9] * 9
    sudoku_list[0] = [str(i) for i in range(1, 10)]
    sudoku_list[4] = [str(i) for i in range(1, 10)]
    sudoku_list[8] = [str(i) for i in range(1, 10)]
    shuffle(sudoku_list[0])
    shuffle(sudoku_list[4])
    shuffle(sudoku_list[8])
    for i in range(len(sudoku_list)):
        sudoku_list[i] = ''.join(sudoku_list[i])
    solved_sudoku = ss.list_to_sudoku(sudoku_list)
    return ss.solve(solved_sudoku)


def removable(cell, sudoku):
    """
    checks if a cell can be removed from the grid keeping it valid (no
    multiple solutions).
    :param cell:
    :param sudoku:
    :param level:
    :return: bool
    """
    sudoku_temp = sudoku.copy()
    sudoku_temp[cell] = '123456789'
    if ss.solve(sudoku_temp)[1] == 'VALID':
        return True


def generate_sudoku(sudoku):
    """
    Considers all the cells in random order. If the sudoku is still
    valid after removal, the cell is removed. If not, it is ignored.
    :param sudoku: complete grid
    :return sudoku: modified grid
    """
    cells = [*sudoku]
    removed_cells = []
    shuffle(cells)
    for cell in cells:
        if removable(cell, sudoku):
            removed_cells.append(cell)
            sudoku[cell] = '123456789'
    # for cell in removed_cells:
    #     sudoku[cell] = ' '
    return sudoku


def grid_to_latex(sudoku, param=0):
    """
    reads the sudoku dictionary and generates a string corresponding to
    each cell value in a latex tabular format
    :param sudoku:
    :return s: the values in a string in latex tabular
    """
    s = ''
    for r in 'ABCDEFGHI':
        for c in '12345678':
            cell = r+c
            value = sudoku[cell]
            if len(value) > 1:
                s = s + '~' + ' & '
            else:
                s = s + value + ' & '
        value = sudoku[r + '9']
        if len(value) >1:
            s = s + '~' + '\\\ \n'
        else:
            s = s + value + '\\\ \n'
        if param == 1:
            s = s + '\\hline \n'
        if r in 'CF':
            s = s + '\\hline \n'
    return s


if __name__ == '__main__':
    solved_sudoku, status = random_grid_generator()
    sudoku = solved_sudoku.copy()
    generate_sudoku(sudoku)
    ss.print_sudoku(sudoku)
    sudoku_eval = sudoku.copy()
    level = ss.eval_level(sudoku_eval)
    status = ss.solve(sudoku_eval)[1]
    print(level, status)
        # generate_sudoku(sudoku)
        # ss.print_sudoku(sudoku)
    problem = grid_to_latex(sudoku, 1)
    solution = grid_to_latex(solved_sudoku)
    with open('problem.tex', 'w') as f:
        f.write(problem)
    with open('solution.tex', 'w') as s_file:
        s_file.write(solution)
    with open('niveau.tex', 'w') as l_file:
        l_file.write(level)
    os.system("pdflatex --interaction=batchmode sudoku.tex")
    os.system("open sudoku.pdf")

