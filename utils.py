def parse_file(filename):
    """parses a dimacs cnf file to a list of clauses

    Args:
        filename (string): cnf file to parse
    """
    clauses = []
    with open(filename, "r") as f:
        for line in f:
            # empty lines and comments are not being parsed
            if line == "" or line[0] == 'c':
                continue
            # currently, the declaration line is not being used
            if line[0] == 'p':
                continue
            clause = [i for i in line[:-2].split()]
            clauses.append(clause)
    return clauses


def print_solution(solution):
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
    