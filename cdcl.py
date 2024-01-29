import copy
from utils import parse_file, print_solution


def check_clauses(clauses: list[list[str]]) -> bool:
    if [] in clauses:
        return False
    only_clauses = [clause for clause in clauses if clause != True]
    if len(only_clauses) == 0:
        return True

    return None


def var_from_literal(literal: str) -> [bool, str]:
    """get the variable of a potentially negated literal

    Args:
        literal (str): literal

    Returns:
        [str, bool]: string is the variable of the literal, bool checks whether the original literal was negated
    """
    if literal[0] == "-":
        return literal[1:], True
    return literal, False


def first_unit_literal(clauses: list[list[str]]) -> [str, int]:
    for i in range(len(clauses)):
        clause = clauses[i]
        if clause != True and len(clause) == 1:
            return clause[0], i
    return "", -1


def remove_assignment_from_clauses(clauses: list[list[str]], var: str, value: bool, antecedents: dict[str|bool, int]):
    if value:
        for i in range(len(clauses)):
            clause = clauses[i]
            if clause == True:
                continue
            if var in clause:
                clauses[i] = True
            elif f"-{var}" in clause:
                clause.remove(f"-{var}")
                if clause == []:
                    antecedents[False] = i
    else:
        for i in range(len(clauses)):
            clause = clauses[i]
            if clause == True:
                continue
            if var in clause:
                clause.remove(var)
                if clause == []:
                    antecedents[False] = i
            elif f"-{var}" in clause:
                clauses[i] = True


def unit_propagation(clauses: list[list[str]], assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int], decision_level: int):
    literal, i = first_unit_literal(clauses)
    while literal:
        var, neg = var_from_literal(literal)
        assignment[var] = [not neg, decision_level]
        antecedents[var] = i
        remove_assignment_from_clauses(clauses, var, not neg, antecedents)
        literal, i = first_unit_literal(clauses)


def propagate(clauses: list[list[str]], assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int], decision_level: int):
    if any(len(clause) == 1 for clause in clauses if clause != True):
        clauses = unit_propagation(clauses, assignment, antecedents, decision_level)


def decide(clauses: list[list[list[str]]], assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int], decision_level: int):
    # We simply assign true to the first variable of the first clause
    first_clause = [clause for clause in clauses if clause != True][0]
    new_assignment = first_clause[0]
    new_assignment, _ = var_from_literal(new_assignment)
    assignment[new_assignment] = [True, decision_level]
    remove_assignment_from_clauses(clauses, new_assignment, True, antecedents)


def get_antecedent_literals(cause: str, assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int]) -> list[str]:
    global original_clauses
    global visited_vars
    # cause - literal of a conflict inducing clause
    cause, _ = var_from_literal(cause)

    visited_vars = visited_vars.union(cause)

    try:
        # cur - clause which is causing assignment of literal cause
        cur = original_clauses[antecedents[cause]]
    except KeyError:
        if assignment[cause][0]:
            return [f"-{cause}"]
        return [cause]

    causes_of = []
    for var in cur:
        if (var[0] == "-" and var[1:] in visited_vars) or var in visited_vars:
            continue
        causes_of.extend(get_antecedent_literals(var, assignment, antecedents))

    return causes_of


def conflict_induced_clause(assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int]) -> list[str]:
    global original_clauses
    global visited_vars
    visited_vars = set()
    try:
        clause = original_clauses[antecedents[False]]
    except KeyError:
        # no conflict
        return []

    causes_of = set()
    for literal in clause:
        cur = get_antecedent_literals(literal, assignment, antecedents)
        causes_of = causes_of.union(cur)
    return list(causes_of)


def decision_levels(clause: list[str], assignment: dict[str, list[bool, int]]) -> list[int]:
    decision_levels = []
    for literal in clause:
        literal, _ = var_from_literal(literal)
        _, level = assignment[literal]
        decision_levels.append(level)
    return decision_levels


def conflict_analysis(assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int]) -> [list[str], int]:
    """analyse the current conflict and determine a level to backtrack to

    Args:
        assignment (dict[str, list[bool, int]]): assignment that led to the conflict
        antecedents (dict[str|bool, int]): antecedents at time the conflict occured

    Returns:
        [list[str], int]: first parameter is the conflict induced clause, the second is backtracking level beta
    """
    clause = conflict_induced_clause(assignment, antecedents)
    if clause == []:
        return [], 0
    beta = max(decision_levels(clause, assignment))
    return clause, beta


def backtracking(beta: int, assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int]):
    """removes all assignments before level b from assignments and antecedents

    Args:
        beta (int): decision level to backtrack to
        assignment (dict[str, list[bool, int]]): current assignments that need to be backtracked
        antecedents (dict[str|bool, int]): current antecedents that need to be backtracked
    """
    vars = list(assignment.keys())
    del antecedents[False]
    for var in vars:
        _, level = assignment[var]
        if level < beta:
            continue
        try:
            del assignment[var]
            del antecedents[var]
        except KeyError:
            pass


def apply_assignment(clauses: list[list[str]], assignment: dict[str, list[bool, int]], antecedents: dict[str|bool, int]):
    for var in assignment.keys():
        value, _ = assignment[var]
        remove_assignment_from_clauses(clauses, var, value, antecedents)


def clear_cic(cic: list[str], assignment: dict[str, list[bool, int]]):
    new_cic = []
    for literal in cic:
        var, neg = var_from_literal(literal)
        if neg:
            if var in assignment.keys() and assignment[var][0]:
                continue
            new_cic.append(literal)
    return new_cic


def cdcl(n_vars: int) -> bool:
    global original_clauses
    # check whether unit propagation yields a conflict -> unsatisfiable
    assignment = {}
    antecedents = {}
    clauses = copy.deepcopy(original_clauses)
    decision_level = 0

    propagate(clauses, assignment, antecedents, decision_level)

    check = check_clauses(clauses)
    if check != None:
        return check

    # while not all variables are assigned
    while len(assignment.keys()) < n_vars:
        copy_clauses = copy.deepcopy(clauses)
        copy_assignment = dict(assignment)
        copy_antecedents = dict(antecedents)
        propagate(copy_clauses, copy_assignment, copy_antecedents, decision_level)

        if [] not in copy_clauses:
            decision_level += 1
            decide(copy_clauses, copy_assignment, copy_antecedents, decision_level)
            propagate(copy_clauses, copy_assignment, copy_antecedents, decision_level)

        check = check_clauses(copy_clauses)
        if check:
            # found satisfying assignment
            print(copy_assignment)
            return True
        elif check == False:
            # current assignments lead to a conflict
            cic, beta = conflict_analysis(copy_assignment, copy_antecedents)
            if beta < 1:
                return False
            original_clauses.append(cic)
            # remove already assigned variables from conflict induced clause
            cic = clear_cic(cic, assignment)
            clauses.append(cic)

            if beta == decision_level:
                decision_level -= 1
                # another unit propagation to get FDA due to conflict induced clause
                # copy because we set these again at the end of our loop
                copy_clauses = copy.deepcopy(clauses)
                copy_assignment = dict(assignment)
                copy_antecedents = dict(antecedents)
            else:
                backtracking(beta, copy_assignment, copy_antecedents)
                # TODO: there must be a better way
                copy_clauses = copy.deepcopy(original_clauses)
                apply_assignment(copy_clauses, copy_assignment, copy_antecedents)
                decision_level = beta - 1
        clauses = copy_clauses
        assignment = copy_assignment
        antecedents = copy_antecedents


# global variables
visited_vars = set()
original_clauses, n_vars = parse_file("sudoku.cnf")
print(cdcl(n_vars))
