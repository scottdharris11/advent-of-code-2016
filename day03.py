"""utility imports"""
from utilities.data import read_lines, parse_integers
from utilities.runner import runner

@runner("Day 3", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    valid = 0
    for line in lines:
        a, b, c, *_ = parse_integers(line, " ")
        if triangle(a, b, c):
            valid += 1
    return valid

@runner("Day 3", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    valid = 0
    for y in range(0, len(lines), 3):
        row1 = parse_integers(lines[y], " ")
        row2 = parse_integers(lines[y+1], " ")
        row3 = parse_integers(lines[y+2], " ")
        for x in range(3):
            if triangle(row1[x], row2[x], row3[x]):
                valid += 1
    return valid

def triangle(a: int, b: int, c: int) -> bool:
    """check if side values can be a triangle"""
    if a + b <= c:
        return False
    if a + c <= b:
        return False
    if b + c <= a:
        return False
    return True

# Data
data = read_lines("input/day03/input.txt")
sample = """5 10 25
5 10 14""".splitlines()
sample2 = """101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603""".splitlines()

# Part 1
assert solve_part1(sample) == 1
assert solve_part1(data) == 1032

# Part 2
assert solve_part2(sample2) == 6
assert solve_part2(data) == 1838
