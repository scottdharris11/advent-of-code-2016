"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 4", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    sectorsum = 0
    for l in lines:
        namei = l.rindex("-")
        csi = l.index("[")
        name = l[:namei]
        sector = int(l[namei+1:csi])
        cs = l[csi+1:l.index("]")]
        letter_counts = {}
        for c in name:
            if c == "-":
                continue
            letter_counts[c] = letter_counts.get(c, 0) + 1
        values = sorted(letter_counts.items(), key=lambda x: (-x[1], x[0]))
        comp = ""
        for i in range(5):
            comp += str(values[i][0])
        if comp == cs:
            sectorsum += sector
    return sectorsum

@runner("Day 4", "Part 2")
def solve_part2(lines: list[str]):
    """part 2 solving function"""
    return 0

# Data
data = read_lines("input/day04/input.txt")
sample = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".splitlines()

# Part 1
assert solve_part1(sample) == 1514
assert solve_part1(data) == 0

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
