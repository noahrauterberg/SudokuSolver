# SudokuSolver

As part of the seminar "Intelligente Software Systeme" at TU Berlin, I've been looking into SAT solvers.
In this repository, I am creating a SAT solver which uses propositional logic in order to solve sudoku puzzles.

> **This project is still work in progress**

## Solvers

- dpll.py: A standard dpll solver. Usage:```python3 dpll.py <filename> <show_solution>```

## Utils

- generate_cnf: Generates a cnf file from a sudoku input, where a dot denotes an empty cell. Usage: ```python3 generate_cnf.py <sudoku_file> <output_file>```
