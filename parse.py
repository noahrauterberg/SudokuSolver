def parse_file(filename):
    """parses a dimacs cnf file

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
