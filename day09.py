"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 9", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    total = 0
    for line in lines:
        d = decompress(line)
        total += len(d)
    return total

@runner("Day 9", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def decompress(s: str) -> str:
    """decompress the supplied string based on the compression rules"""
    r = re.compile(r'\(([\d]+)x([\d]+)\)')
    out = ""
    begin = 0
    while True:
        m = r.search(s, begin)
        if m is None:
            break
        out += s[begin:m.start()]
        length = int(m.group(1))
        times = int(m.group(2))
        seq = s[m.end():m.end()+length]
        out += seq * times
        begin = m.end()+length
    out += s[begin:]
    return out

# Data
data = read_lines("input/day09/input.txt")

# Part 1
assert decompress("ADVENT") == "ADVENT"
assert decompress("A(1x5)BC") == "ABBBBBC"
assert decompress("(3x3)XYZ") == "XYZXYZXYZ"
assert decompress("A(2x2)BCD(2x2)EFG") == "ABCBCDEFEFG"
assert decompress("(6x1)(1x3)A") == "(1x3)A"
assert decompress("X(8x2)(3x3)ABCY") == "X(3x3)ABC(3x3)ABCY"
assert solve_part1(data) == 120765

# Part 2
assert solve_part2(data) == 0
