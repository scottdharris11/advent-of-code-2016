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
    total = 0
    for line in lines:
        total += decompress_v2_length(line)
    return total

marker = re.compile(r'\(([\d]+)x([\d]+)\)')

def decompress(s: str) -> str:
    """decompress the supplied string based on the compression rules"""
    out = ""
    begin = 0
    while True:
        m = marker.search(s, begin)
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

def decompress_v2_length(s: str) -> int:
    """using v2 rules, determine length of decompressed string"""
    length = 0
    begin = 0
    while True:
        m = marker.search(s, begin)
        if m is None:
            break
        length += m.start()-begin
        seqlen = int(m.group(1))
        times = int(m.group(2))
        length += decompress_v2_length(s[m.end():m.end()+seqlen]) * times
        begin = m.end()+seqlen
    length += len(s) - begin
    return length

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
assert decompress_v2_length("(3x3)XYZ") == 9
assert decompress_v2_length("X(8x2)(3x3)ABCY") == 20
assert decompress_v2_length("(27x12)(20x12)(13x14)(7x10)(1x12)A") == 241920
assert decompress_v2_length("(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN") == 445
assert solve_part2(data) == 11658395076
