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


def removable(cell, sudoku, level=3):
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
    if ss.solve(sudoku_temp, level)[1] == 'VALID':
        return True


def generate_sudoku(sudoku, level=3):
    cells = [*sudoku]
    removed_cells = []
    shuffle(cells)
    for cell in cells:
        if removable(cell, sudoku, level):
            print(cell)
            removed_cells.append(cell)
            sudoku[cell] = '123456789'
    print(len(removed_cells))
    for cell in removed_cells:
        sudoku[cell] = ' '
    return sudoku


def grid_to_latex(sudoku):
    s = ''
    for r in 'ABCDEFGHI':
        for c in '12345678':
            cell = r+c
            s = s + sudoku[cell] + ' & '
        s = s + sudoku[r + '9'] + '\\\ \n\\hline \n'
        if r in 'CF':
            s = s+ '\\hline \n'
    return s


if __name__ == '__main__':
    solved_sudoku, status = random_grid_generator()
    ss.print_sudoku(solved_sudoku)
    print(status)
    sudoku = solved_sudoku.copy()
    generate_sudoku(sudoku)
    ss.print_sudoku(sudoku)
    problem = grid_to_latex(sudoku)
    solution = grid_to_latex(solved_sudoku)
    with open('problem.tex', 'w') as f:
        f.write(problem)
    with open('solution.tex', 'w') as s_file:
        s_file.write(solution)
    os.system("pdflatex --interaction=batchmode sudoku.tex")
    os.system("open sudoku.pdf")