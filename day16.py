"""utility imports"""
import functools
from utilities.runner import runner

@runner("Day 16", "Part 1")
def solve_part1(init: str, disk_size: int) -> str:
    """part 1 solving function"""
    return fill_and_check(init, disk_size)

@runner("Day 16", "Part 2")
def solve_part2(init: str, disk_size: int) -> str:
    """part 2 solving function"""
    return fill_and_check(init, disk_size)

def fill_and_check(init: str, disk_size: int) -> str:
    """generate fill and check sum for supplied disk size"""
    work = []
    work.append(init)
    work_size = len(init)
    prev_reverse = ""
    while work_size < disk_size:
        prev_reverse = dragonc(work, prev_reverse)
        csize = len(work[-1])
        work_size += csize
        if work_size > disk_size:
            cut = csize - (work_size-disk_size)
            work[-1] = work[-1][:cut]
        #print(work_size)
    cs = chunked_checksum("".join(work))
    while len(cs) % 2 == 0:
        cs = chunked_checksum(cs)
        #print(len(cs))
    return cs

def dragon(a: str) -> str:
    """dragon curve a supplied str"""
    chunks = []
    chunks.append(a)
    dragonc(chunks, "")
    return "".join(chunks)

def dragonc(chunks: list[str], pr: str) -> str:
    """build next chunk of a dragon stream"""
    c = chunks[-1]
    r = chunked_reverse(c) + pr
    chunks.append("0" + r)
    return r

def chunked_reverse(a:str) -> str:
    """perform reversal of supplied string in chunks"""
    cr = ""
    for end in range(len(a), -1, -10):
        start = end - 10
        if start < 0:
            start = 0
        cr += reverse(a[start:end])
    return cr

@functools.cache
def reverse(a: str) -> str:
    """reverse and switch values of supplied string"""
    b = ""
    for i in range(len(a)-1,-1,-1):
        b = b + "1" if a[i] == "0" else b + "0"
    return b

def chunked_checksum(a:str) -> str:
    """build checksum by chunking input string"""
    cs = ""
    for start in range(0, len(a), 10):
        cs += checksum(a[start:start+10])
    return cs

@functools.cache
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
assert solve_part2("11110010111001001", 35651584) == "11001111011000111"
