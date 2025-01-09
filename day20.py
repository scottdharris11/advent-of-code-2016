"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 20", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    dblocks = parse_deny_blocks(lines)
    return dblocks[0][1] + 1

@runner("Day 20", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def parse_deny_blocks(lines: list[str]) -> list[tuple[int,int]]:
    """parse the deny blocks from input into an ordered list with overlaps resolved"""
    # capture each beginning in list (which we will sort) and each referenced end
    begins = []
    ends = {}
    for line in lines:
        s, e = map(int, line.split("-"))
        begins.append(s)
        ends[s] = e
    begins.sort()

    # work through each beginning block collapsing ranges that overlap
    dblocks = []
    bidx = 0
    blen = len(begins)
    while bidx < blen:
        bb = begins[bidx]
        ee = ends[bb]
        eidx = bidx
        while eidx + 1 < blen and (begins[eidx+1] < ee or ee + 1 == begins[eidx+1]):
            eidx += 1
            if ends[begins[eidx]] > ee:
                ee = ends[begins[eidx]]
        dblocks.append((bb, ee))
        bidx = eidx + 1
    return dblocks

# Data
data = read_lines("input/day20/input.txt")
sample = """5-8
0-2
4-7""".splitlines()

# Part 1
assert solve_part1(sample) == 3
assert solve_part1(data) == 14975795

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
