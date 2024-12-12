"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

keypad = [[1, 2, 3],[4, 5, 6],[7, 8, 9]]
moves = {'U':(0,-1), 'L':(-1,0), 'R':(1,0), 'D':(0,1)}

@runner("Day 2", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    code = ""
    loc = (1,1)
    for line in lines:
        loc = move(loc, line)
        code += str(keypad[loc[1]][loc[0]])
    return int(code)

@runner("Day 2", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

def move(start: Tuple[int, int], instructions: str) -> Tuple[int, int]:
    """move from starting location based on instructions"""
    loc = start
    for i in instructions:
        adjust = moves[i]
        x = loc[0] + adjust[0]
        if x < 0:
            x = 0
        if x > 2:
            x = 2
        y = loc[1] + adjust[1]
        if y < 0:
            y = 0
        if y > 2:
            y = 2
        loc = (x, y)
    return loc

# Data
data = read_lines("input/day02/input.txt")
sample = """ULL
RRDDD
LURDL
UUUUD""".splitlines()

# Part 1
assert solve_part1(sample) == 1985
assert solve_part1(data) == 47978

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
