from z3 import *

s = Solver()

grid = [
    [Int(f"cell_{i}_{j}") for j in range(9)] for i in range(9)
]

for i in range(9):
    for j in range(9):
        s.add(grid[i][j] >= 1, grid[i][j] <= 9)
    s.add(Distinct(grid[i]))
    
for j in range(9):
    s.add(Distinct([grid[i][j] for i in range(9)]))

for x in range(3):
    for y in range(3):
        s.add(Distinct([
            grid[x*3][y*3],
            grid[x*3][y*3+1],
            grid[x*3][y*3+2],
            grid[x*3+1][y*3],
            grid[x*3+1][y*3+1],
            grid[x*3+1][y*3+2],
            grid[x*3+2][y*3],
            grid[x*3+2][y*3+1],
            grid[x*3+2][y*3+2]
        ]))

# dot denotes an empty cell
"""
sudoku = [
    ".34.9....",
    "...7..6..",
    ".1.......",
    "8.....5.9",
    "6....3...",
    "....1....",
    ".......14",
    "5..8.....",
    ".......2."
]
sudoku = [
    "5..4.79.3",
    "..2.1..87",
    "1..68...4",
    "8..3..7..",
    ".26..1345",
    "47..5....",
    "....324.9",
    ".3...8.62",
    "..976.5.8"
]
"""
sudoku = [
    "....681..",
    "1.....7..",
    ".432..5..",
    "3.....4..",
    "8.......9",
    "..1.....6",
    "..6..485.",
    "..2.....7",
    ".1.59...."
]

for i in range(9):
    for j in range(9):
        n = sudoku[i][j]
        if n != '.':
            s.add(grid[i][j] == int(n))

result = s.check()
if result == sat:
    m = s.model()

    for i in range(9):
        print("".join(str(m.eval(grid[i][j])) for j in range(9)))
else:
    print("unsatisfiable")
    