def parse_file(filename: str) -> [list[list[str]], int]:
    """parses a DIMACS cnf file to a list of clauses

    Args:
        filename (string): cnf file to parse
    Returns:
        clauses: 2D-List of clauses
        n_vars: number of variables used - None if not given
    """
    clauses = []
    with open(filename, "r") as f:
        n_vars = 0
        for line in f:
            # empty lines and comments are not being parsed
            if line == "" or line[0] == 'c':
                continue
            # currently, the declaration line is not being used
            if line[0] == 'p':
                n_vars = int(line.split(" ")[2])
                continue
            clause = [i for i in line[:-2].split()]
            clauses.append(clause)
    return clauses, n_vars


def print_solution(solution):
    """Prints the solution as a sudoku grid

    Args:
        solution ([string]): list of true variable names following the form "x_{r}_{c}_{n}" 
        where the number n is written in the cell in row r and column c
    """
    solution = sorted(solution)
    
    print("Solution to the Sudoku:\n")
    row = 0
    col = 0
    for i in solution:
        if row > 8:
            row = 0
            col += 1
            print("\n" if  col != 0 and col % 3 == 0 else "")
        n = i[2:].split('_')[2]
        print(f"{n} " if row % 3 == 2 else n, end="")
        row += 1
    print()
