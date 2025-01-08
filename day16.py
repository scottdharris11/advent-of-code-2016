"""utility imports"""
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(init: str, disk_size: int) -> str:
    """part 1 solving function"""
    work = init
    while len(work) < disk_size:
        work = dragon(work)
        if len(work) > disk_size:
            work = work[:disk_size]
    cs = checksum(work)
    while len(cs) % 2 == 0:
        cs = checksum(cs)
    return cs

@runner("Day 16", "Part 2")
def solve_part2(init: str, disk_size: int) -> str:
    """part 2 solving function"""
    return ""

def dragon(a: str) -> str:
    """dragon curve a supplied str"""
    b = a + "0"
    for i in range(len(a)-1,-1,-1):
        b = b + "1" if a[i] == "0" else b + "0"
    return b

def checksum(a: str) -> str:
    """build checksum for a string"""
    cs = ""
    for i in range(0, len(a)-1, 2):
        cs = cs + "1" if a[i] == a[i+1] else cs + "0"
    return cs

# Function Tests
assert dragon("1") == "100"
assert dragon("0") == "001"
assert dragon("11111") == "11111000000"
assert dragon("111100001010") == "1111000010100101011110000"

assert checksum("110010110100") == "110101"
assert checksum("110101") == "100"

# Part 1
assert solve_part1("10000", 20) == "01100"
assert solve_part1("11110010111001001", 272) == "01110011101111011"

# Part 2
assert solve_part2("11110010111001001", 272) == ""
