"""utility imports"""
import hashlib
from utilities.runner import runner

@runner("Day 5", "Part 1")
def solve_part1(door_id: str) -> str:
    """part 1 solving function"""
    idx = 0
    pwd = ""
    while True:
        key = door_id + str(idx)
        h = hashlib.md5(key.encode())
        d = h.hexdigest()
        if d[0:5] == "00000":
            pwd += d[5]
            if len(pwd) == 8:
                break
        idx += 1
    return pwd

@runner("Day 5", "Part 2")
def solve_part2(door_id: str) -> str:
    """part 2 solving function"""
    idx = 0
    pwd = [" "] * 8
    filled = 0
    while True:
        key = door_id + str(idx)
        h = hashlib.md5(key.encode())
        d = h.hexdigest()
        if d[0:5] == "00000" and str(d[5]).isdigit() and int(d[5]) < 8 and pwd[int(d[5])] == " ":
            pwd[int(d[5])] = d[6]
            filled += 1
            if filled == 8:
                break
        idx += 1
    return "".join(pwd)

# Data
DATA = "uqwqemis"
SAMPLE = "abc"

# Part 1
assert solve_part1(SAMPLE) == "18f47a30"
assert solve_part1(DATA) == "1a3099aa"

# Part 2
assert solve_part2(SAMPLE) == "05ace8e3"
assert solve_part2(DATA) == "694190cd"
