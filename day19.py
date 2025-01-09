"""utility imports"""
from utilities.runner import runner

@runner("Day 19", "Part 1")
def solve_part1(count: int) -> int:
    """part 1 solving function"""
    first = Elf(1)
    last = first
    for ei in range(2,count+1):
        elf = Elf(ei)
        last.next_elf = elf
        last = elf
    last.next_elf = first

    current = first
    while current.elfid != current.next_elf.elfid:
        current.presents += current.next_elf.presents
        current.next_elf = current.next_elf.next_elf
        current = current.next_elf
    return current.elfid

@runner("Day 19", "Part 2")
def solve_part2(count: int) -> int:
    """part 2 solving function"""
    return 0

class Elf:
    """elf definition"""
    def __init__(self, elfid: int):
        self.elfid = elfid
        self.presents = 1
        self.next_elf = None

# Part 1
assert solve_part1(5) == 3
assert solve_part1(3017957) == 1841611

# Part 2
assert solve_part2(5) == 0
assert solve_part2(3017957) == 0
