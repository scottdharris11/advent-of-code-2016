"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

directions = [(0,1),(1,0),(0,-1),(-1,0)]

@runner("Day 1", "Part 1")
def solve_part1(instructions: list[str]):
    """part 1 solving function"""
    pos = [0,0]
    cur = 0
    for i in instructions:
        if i[0] == 'R':
            cur = (cur + 1) % 4
        else:
            cur = (cur - 1) % 4
        steps = int(i[1:])
        pos[0] += directions[cur][0] * steps
        pos[1] += directions[cur][1] * steps
    return abs(pos[0]) + abs(pos[1])

@runner("Day 1", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day01/input.txt")[0].split(", ")
sample = """R2, L3""".split(", ")
sample2 = """R2, R2, R2""".split(", ")
sample3 = """R5, L5, R5, R3""".split(", ")

# Part 1
assert solve_part1(sample) == 5
assert solve_part1(sample2) == 2
assert solve_part1(sample3) == 12
assert solve_part1(data) == 242

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
