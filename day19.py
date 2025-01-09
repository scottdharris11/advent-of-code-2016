"""utility imports"""
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(count: int) -> int:
    """part 1 solving function"""
    current = build_elf_circle(count)
    while current.elfid != current.next_elf.elfid:
        next_elf = current.next_elf
        current.presents += next_elf.presents
        current.next_elf = next_elf.next_elf
        current = current.next_elf
    return current.elfid

@runner("Day 19", "Part 2")
def solve_part2(count: int) -> int:
    """part 2 solving function"""
    current = build_elf_circle(count)
    across = current
    for _ in range(count // 2):
        across = across.next_elf
    ccount = count
    while ccount > 1:
        current.presents += across.presents
        across.prev_elf.next_elf = across.next_elf
        across.next_elf.prev_elf = across.prev_elf
        across = across.next_elf
        if ccount % 2 == 1:
            across = across.next_elf
        ccount -= 1
        current = current.next_elf
    return current.elfid

class Elf:
    """elf definition"""
    def __init__(self, elfid: int):
        self.elfid = elfid
        self.presents = 1
        self.next_elf = None
        self.prev_elf = None

    def __repr__(self):
        return str((self.elfid, self.presents, self.prev_elf.elfid, self.next_elf.elfid))

def build_elf_circle(count: int) -> Elf:
    """build circle of elves based on supplied elf count"""
    first = Elf(1)
    last = first
    for ei in range(2,count+1):
        elf = Elf(ei)
        elf.prev_elf = last
        last.next_elf = elf
        last = elf
    last.next_elf = first
    first.prev_elf = last
    return first

# Part 1
assert solve_part1(5) == 3
assert solve_part1(3017957) == 1841611

# Part 2
assert solve_part2(5) == 2
assert solve_part2(3017957) == 1423634
