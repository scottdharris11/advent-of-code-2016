"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 4", "Part 1")
def solve_part1(lines: list[str]):
    """part 1 solving function"""
    sectorsum = 0
    for line in lines:
        name, sector, cs = parse(line)
        if valid(name, cs):
            sectorsum += sector
    return sectorsum

@runner("Day 4", "Part 2")
def solve_part2(lines: list[str], match: str):
    """part 2 solving function"""
    for line in lines:
        name, sector, cs = parse(line)
        if not valid(name, cs):
            continue
        dname = ""
        offset = sector % 26
        for c in name:
            if c == "-":
                dname += " "
            else:
                o = ord(c) + offset
                if o > ord('z'):
                    o = ord('a') + o - ord('z') - 1
                dname += chr(o)
        if dname == match:
            return sector
    return 0

def parse(s: str) -> tuple[str,int,str]:
    """parse values from string"""
    namei = s.rindex("-")
    csi = s.index("[")
    return (s[:namei], int(s[namei+1:csi]), s[csi+1:s.index("]")])

def valid(name: str, cs: str) -> bool:
    """check if data is valid"""
    letter_counts = {}
    for c in name:
        if c == "-":
            continue
        letter_counts[c] = letter_counts.get(c, 0) + 1
    values = sorted(letter_counts.items(), key=lambda x: (-x[1], x[0]))
    comp = ""
    for i in range(5):
        comp += str(values[i][0])
    return comp == cs

# Data
data = read_lines("input/day04/input.txt")
sample = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]""".splitlines()

# Part 1
assert solve_part1(sample) == 1514
assert solve_part1(data) == 185371

# Part 2
assert solve_part2(["qzmt-zixmtkozy-ivhz-343[zimth]"], "very encrypted name") == 343
assert solve_part2(data, "northpole object storage") == 984
