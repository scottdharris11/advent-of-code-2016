"""utility imports"""
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(init: str, disk_size: int) -> str:
    """part 1 solving function"""
    return 0

@runner("Day 16", "Part 2")
def solve_part2(init: str, disk_size: int) -> str:
    """part 2 solving function"""
    return 0

# Part 1
assert solve_part1("10000", 20) == "01100"
assert solve_part1("11110010111001001", 272) == ""

# Part 2
assert solve_part1("11110010111001001", 272) == ""
