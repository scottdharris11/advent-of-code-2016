"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 15", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    discs = parse_discs(lines)
    return drop_time(discs)

@runner("Day 15", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    discs = parse_discs(lines)
    discs.append((len(discs)+1, 11, 0))
    return drop_time(discs)

def parse_discs(lines: list[str]) -> tuple[int,int,int]:
    """parse disc entries from lines"""
    r = re.compile(r"Disc #([\d]+) has ([\d]+) positions; at time=0, it is at position ([\d]+)\.")
    discs = []
    for line in lines:
        m = r.match(line)
        discs.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    return discs

def drop_time(discs: list[tuple[int,int,int]]) -> int:
    """calculate the drop time to get through all slots"""
    seconds = 0
    adjust = 0
    max_size = -1
    for disc in discs:
        time_offset, size, time_0 = disc
        if max_size == -1 or size > max_size:
            seconds = zero_offset(disc)
            adjust = max_size = size
    while True:
        for disc in discs:
            time_offset, size, time_0 = disc
            slot = (time_0 + seconds + time_offset) % size
            if slot != 0:
                break
        else:
            break
        seconds += adjust
    return seconds

def zero_offset(disc: tuple[int,int,int]) -> int:
    """calculate the offset to position zero for a disc with a particular time offset"""
    time_offset, size, time_0 = disc
    return size - ((time_0 + time_offset) % size)

# Data
data = read_lines("input/day15/input.txt")
sample = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""".splitlines()

# Part 1
assert solve_part1(sample) == 5
assert solve_part1(data) == 122318

# Part 2
assert solve_part2(data) == 3208583
