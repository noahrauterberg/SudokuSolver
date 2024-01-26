import sys
from z3 import *


def parse_sudoku(filename):
    allowed_chars = set("123456789.\n")
    sudoku = []
    with open(filename, "r") as f:
        for line in f:
            if len(line) > 10 or not set(line).issubset(allowed_chars):
                print("input file is no valid sudoku")
                return None
            sudoku.append(line[:-1])
    if len(sudoku) > 9:
        print("input file is no valid sudoku")
        return None


def write_cnf(file, clause, end):
    if is_not(clause):
        file.write(f"-{clause.children()[0]}{end}")
    elif is_or(clause):
        for child in clause.children():
            write_cnf(file, child, " ")
        file.write(" 0\n")
    else:
        file.write(f"{clause}{end}")


def cnf_to_file(filename, formular):
    """Generates a file almost in the DIMACS cnf format, but variables have complete names instead of just numbers

    Args:
        filename (string): name of the file where the cnf formular is being written
    """
    with open(filename, "w") as f:
        # the first line of the file gives some information on the formular
        f.write(f"p cnf 729 {len(formular[0])}\n")
        for clause in formular[0]:
            write_cnf(f, clause, " 0\n")


def constraints(sudoku):
    s = Solver()
    variables = [
        [
            [Bool(f"x_{i}_{j}_{c}") for c in range(1, 10)] for j in range(9)
        ] for i in range(9)
    ]

    # exactly one number per cell
    for i in range(9):
        for j in range(9):
            # at least one per cell is true
            s.add(Or(*[variables[i][j][c] for c in range(9)]))
            # if one is true, no other can be true
            for c in range(9):
                for d in range(9):
                    if c == d:
                        continue
                    s.add(Implies(variables[i][j][c], Not(variables[i][j][d])))

    # every number only once per column
    for i in range(9):
        for j in range(8):
            for k in range(j+1, 9):
                for c in range(9):
                    s.add(Not(And(variables[i][j][c], variables[i][k][c])))

    # every number only once per row
    for j in range(9):
        for i in range(8):
            for k in range(i+1, 9):
                for c in range(9):
                    s.add(Not(And(variables[i][j][c], variables[k][j][c])))

    # every number only once per block
    for i in range(9):
        for j in range(9):
            for c in range(9):
                s.add(Or(*[variables[i][j][c] for c in range(9)]))
                for i_prime in range(9):
                    for j_prime in range(9):
                        if (i // 3 == i_prime // 3 and j // 3 == j_prime // 3 and (i, j) != (i_prime, j_prime)):
                            s.add(Implies(variables[i][j][c], Not(
                                variables[i_prime][j_prime][c])))

    # add given numbers
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != '.':
                s.add(variables[i][j][int(sudoku[i][j]) - 1])

    # convert to cnf
    t = Tactic('tseitin-cnf')
    goal = Goal()
    goal.add(s.assertions())
    if s.check():
        print("Sudoku is valid")
    else:
        print("Sudoku is invalid")
    return t(goal)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Correct usage: python3 generate_cnf.py <sudoku_file> <output_file>")
        sys.exit()
    if len(sys.argv) < 3:
        output_file = "sudoku.cnf"
    else:
        output_file = sys.argv[2]

    input_file = sys.argv[1]
    sudoku = parse_sudoku(input_file)
    if not sudoku:
        sys.exit()
    cnf = constraints(sudoku)
    cnf_to_file(output_file, cnf)
