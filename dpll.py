import copy
import sys
from utils import parse_file, print_solution

satisfying_assignment = {}


def remove_assignment_from_clauses(clauses, assignment_variable, value):
    # TODO: simplify
    if value:
        new_clauses = []
        for clause in clauses:
            if assignment_variable in clause:
                continue
            if f"-{assignment_variable}" in clause:
                clause.remove(f"-{assignment_variable}")
            new_clauses.append(clause)
    else:
        new_clauses = []
        for clause in clauses:
            if f"-{assignment_variable}" in clause:
                continue
            if assignment_variable in clause:
                clause.remove(assignment_variable)
            new_clauses.append(clause)
    return new_clauses


def unit_propagation(clauses, assignment):
    unit_literals = [c[0] for c in clauses if len(c) == 1]
    while len(unit_literals) > 0:
        # assign literal to true
        if unit_literals[0][0] == '-':
            assignment[unit_literals[0][1:]] = False
            clauses = remove_assignment_from_clauses(
                clauses, unit_literals[0][1:], False)
        else:
            assignment[unit_literals[0]] = True
            clauses = remove_assignment_from_clauses(
                clauses, unit_literals[0], True)
        # due to the unit clause rule, new unit clauses could have been formed or others might have become obsolete
        unit_literals = [c[0] for c in clauses if len(c) == 1]
    return clauses


def dpll(clauses, assignment):
    global satisfying_assignment
    if len(clauses) == 0:
        satisfying_assignment = assignment
        return True
    if [] in clauses:
        return False

    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    if len(unit_clauses) > 0:
        clauses = unit_propagation(clauses, assignment)
        return dpll(clauses, dict(assignment))
    else:
        # always assign the first literal
        new_assignment = clauses[0][0]
        if new_assignment[0] == '-':
            new_assignment = new_assignment[1:]

        return dpll(copy.deepcopy(clauses) + [[new_assignment]], dict(assignment)) or dpll(copy.deepcopy(clauses) + [[f"-{new_assignment}"]], dict(assignment))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Correct usage: python3 dpll.py <filename> <show_solution>")
        sys.exit()
    if len(sys.argv) < 3:
        show_solution = False
    else:
        show_solution = sys.argv[2].lower()
        if show_solution == "true":
            show_solution = True
        elif show_solution == "false":
            show_solution = False
        else:
            print("Correct usage: python3 dpll.py <filename> <show_solution>")
            sys.exit()

    filename = sys.argv[1]
    formular = parse_file(filename)
    sat = dpll(formular, {})
    if sat and show_solution:
        solution = [var for var in satisfying_assignment.keys() if satisfying_assignment[var]]
        print_solution(solution)
    elif sat:
        print("Formular is satisfiable")
    else:
        print("Formular is unsatisfiable")
