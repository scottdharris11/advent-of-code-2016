"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 6", "Part 1")
def solve_part1(lines: list[str]) -> str:
    """part 1 solving function"""
    counts = counts_by_index(lines)
    output = ""
    for ci in counts:
        h = 0
        hc = ""
        for c, count in ci.items():
            if h == 0 or count > h:
                h = count
                hc = c
        output += hc
    return output

@runner("Day 6", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    counts = counts_by_index(lines)
    output = ""
    for ci in counts:
        l = 0
        lc = ""
        for c, count in ci.items():
            if l == 0 or count < l:
                l = count
                lc = c
        output += lc
    return output

def counts_by_index(lines: list[str]) -> list[dict[chr,int]]:
    """count the character occurences in each column of each line"""
    counts = []
    for _ in range(len(lines[0])):
        counts.append({})
    for line in lines:
        for i, c in enumerate(line):
            ci = counts[i]
            cc = ci.get(c,0)
            ci[c] = cc + 1
    return counts

# Data
data = read_lines("input/day06/input.txt")
sample = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar""".splitlines()

# Part 1
assert solve_part1(sample) == "easter"
assert solve_part1(data) == "mshjnduc"

# Part 2
assert solve_part2(sample) == "advent"
assert solve_part2(data) == "apfeeebz"
