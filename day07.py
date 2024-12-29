"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 7", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    r = re.compile(r'(\[[a-z]*?\])')
    tls = 0
    for line in lines:
        hypernets = r.findall(line)
        for h in hypernets:
            if abba(h[1:len(h)-1]):
                break
        else:
            for s in r.sub('|', line).split('|'):
                if abba(s):
                    tls += 1
                    break
    return tls

@runner("Day 7", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def abba(s: str) -> bool:
    """determine if abba exists within string"""
    if len(s) < 4:
        return False
    for i in range(len(s)-3):
        if s[i] != s[i+2] and s[i] == s[i+3] and s[i+1] == s[i+2]:
            return True
    return False

# Data
data = read_lines("input/day07/input.txt")
sample = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn""".splitlines()

# Part 1
assert solve_part1(sample) == 2
assert solve_part1(data) == 105

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
