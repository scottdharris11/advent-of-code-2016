"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 18", "Part 1")
def solve_part1(first: str, rows: int) -> int:
    """part 1 solving function"""
    return safe_tiles(first, rows)

@runner("Day 18", "Part 2")
def solve_part2(first: str) -> int:
    """part 2 solving function"""
    return safe_tiles(first, 400000)

def safe_tiles(first: str, rows: int) -> int:
    """count the total amount of safe tiles"""
    length = len(first)
    safe = first.count(SAFE)
    tiles = first
    for _ in range(rows-1):
        tiles = plot_tiles(tiles, length)
        safe += tiles.count(SAFE)
    return safe

SAFE = '.'
TRAP = '^'
TRAP_RULES = {TRAP+TRAP+SAFE: 1, SAFE+TRAP+TRAP: 1, TRAP+SAFE+SAFE: 1, SAFE+SAFE+TRAP: 1}

def plot_tiles(prev: str, length: int) -> str:
    """plot the tiles based on the previous tile row"""
    tiles = ""
    for i in range(length):
        check = ""
        if i == 0:
            check = SAFE + prev[i:i+2]
        elif i == length-1:
            check = prev[i-1:i+1] + SAFE
        else:
            check = prev[i-1:i+2]
        tiles = tiles + TRAP if check in TRAP_RULES else tiles + SAFE
    return tiles

# Data
data = read_lines("input/day18/input.txt")
sample = """..^^.
.^^^^
^^..^""".splitlines()
sample2 = """.^^.^.^^^^
^^^...^..^
^.^^.^.^^.
..^^...^^^
.^^^^.^^.^
^^..^.^^..
^^^^..^^^.
^..^^^^.^^
.^^^..^.^^
^^.^^^..^^""".splitlines()

for t in range(0, len(sample)-1, 1):
    assert plot_tiles(sample[t],len(sample[t])) == sample[t+1]
for t in range(0, len(sample2)-1, 1):
    assert plot_tiles(sample2[t],len(sample2[t])) == sample2[t+1]

# Part 1
assert solve_part1(sample[0],3) == 6
assert solve_part1(sample2[0],10) == 38
assert solve_part1(data[0], 40) == 2016

# Part 2
assert solve_part2(data[0]) == 19998750
