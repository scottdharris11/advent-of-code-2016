"""utility imports"""
from typing import Tuple
from utilities.data import read_lines
from utilities.runner import runner

keypad = [["1", "2", "3"],["4", "5", "6"],["7", "8", "9"]]
keypad2 = [
    ["X", "X", "1", "X", "X"],
    ["X", "2", "3", "4", "X"],
    ["5", "6", "7", "8", "9"],
    ["X", "A", "B", "C", "X"],
    ["X", "X", "D", "X", "X"]
]
moves = {'U':(0,-1), 'L':(-1,0), 'R':(1,0), 'D':(0,1)}

@runner("Day 2", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    code = ""
    loc = (1,1)
    for line in lines:
        loc = move(keypad, loc, line)
        code += keypad[loc[1]][loc[0]]
    return code

@runner("Day 2", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    code = ""
    loc = (0,2)
    for line in lines:
        loc = move(keypad2, loc, line)
        code += keypad2[loc[1]][loc[0]]
    return code

def move(pad: list[list[str]], start: Tuple[int, int], instructions: str) -> Tuple[int, int]:
    """move from starting location based on instructions"""
    loc = start
    for i in instructions:
        adjust = moves[i]
        y = loc[1] + adjust[1]
        if y < 0:
            y = 0
        if y >= len(pad):
            y = len(pad)-1
        if pad[y][loc[0]] == 'X':
            y = loc[1]

        x = loc[0] + adjust[0]
        if x < 0:
            x = 0
        if x >= len(pad[0]):
            x = len(pad[0])-1
        if pad[y][x] == 'X':
            x = loc[0]

        loc = (x, y)
    return loc

# Data
data = read_lines("input/day02/input.txt")
sample = """ULL
RRDDD
LURDL
UUUUD""".splitlines()

# Part 1
assert solve_part1(sample) == "1985"
assert solve_part1(data) == "47978"

# Part 2
assert solve_part2(sample) == "5DB3"
assert solve_part2(data) == "659AD"
