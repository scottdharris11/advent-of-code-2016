"""utility imports"""
import hashlib
from utilities.runner import runner

@runner("Day 14", "Part 1")
def solve_part1(salt: str) -> int:
    """part 1 solving function"""
    keys = []
    candidates = {}
    d = 0
    while True:
        s = salt + str(d)
        h = hashlib.md5(s.encode()).hexdigest()
        didx = []
        for k, v in candidates.items():
            if h.find(v[1]) >= 0:
                keys.append((k,h))
                didx.append(k)
                if len(keys) == 64:
                    break
            elif d == k + 1000:
                didx.append(k)
        if len(keys) == 64:
            break
        for k in didx:
            del candidates[k]
        repeat = find_repeating(h)
        if repeat[0]:
            candidates[d] = (h, repeat[1]*5)
        d += 1
    return keys[-1][0]

@runner("Day 14", "Part 2")
def solve_part2(salt: str) -> int:
    """part 2 solving function"""
    return 0

def find_repeating(s: str) -> tuple[bool,chr]:
    """check string for a repeating character (3 times)"""
    for i in range(2,len(s)):
        if s[i] == s[i-1] == s[i-2]:
            return (True,s[i])
    return (False,None)

# Part 1
assert solve_part1("abc") == 22728
assert solve_part1("ngcjuoqr") == 18626

# Part 2
assert solve_part2("abc") == 0
assert solve_part2("ngcjuoqr") == 0
