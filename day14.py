"""utility imports"""
import hashlib
from utilities.runner import runner

@runner("Day 14", "Part 1")
def solve_part1(salt: str) -> int:
    """part 1 solving function"""
    key_indexes = gen_keys(salt, False)
    return key_indexes[-1]

@runner("Day 14", "Part 2")
def solve_part2(salt: str) -> int:
    """part 2 solving function"""
    key_indexes = gen_keys(salt, True)
    return key_indexes[-1]

def gen_keys(salt: str, stretch: bool) -> list[int]:
    """generate 64 keys for the supplied salt"""
    keys = []
    candidates = []
    d = 0
    stop = False
    while True:
        h = compute_key(salt, d, stretch)
        didx = []
        for ci, c in enumerate(candidates):
            k, r = c
            if h.find(r) >= 0:
                keys.append(k)
                didx.append(ci)
                if len(keys) == 64:
                    stop = True
            elif d == k + 1000:
                didx.append(ci)
        for offset, index in enumerate(didx):
            candidates.pop(index-offset)
        if stop and len(candidates) == 0:
            break
        if not stop:
            repeat = find_repeating(h)
            if repeat[0]:
                candidates.append((d,repeat[1]*5))
        d += 1
    keys.sort()
    return keys[:64]

def find_repeating(s: str) -> tuple[bool,chr]:
    """check string for a repeating character (3 times)"""
    for i in range(2,len(s)):
        if s[i] == s[i-1] == s[i-2]:
            return (True,s[i])
    return (False,None)

def compute_key(salt: str, index: int, stretch: bool) -> str:
    """compute the key for the supplied index and salt"""
    s = salt + str(index)
    h = hashlib.md5(s.encode()).hexdigest()
    if stretch:
        for _ in range(2016):
            h = hashlib.md5(h.encode()).hexdigest()
    return h

# Part 1
assert solve_part1("abc") == 22728
assert solve_part1("ngcjuoqr") == 18626

# Part 2
assert solve_part2("abc") == 22551
assert solve_part2("ngcjuoqr") == 20092
