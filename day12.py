"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 12", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    registers = {}
    instructions = parse_instructions(lines, registers)
    max_idx = len(instructions)-1
    idx = 0
    while True:
        idx = instructions[idx].execute(idx, registers)
        if idx > max_idx:
            break
    return registers["a"]

@runner("Day 12", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class Instruction:
    """definition for instruction"""
    def __init__(self, line: str, registers: dict[str,int]):
        pieces = line.split(" ")
        self.ins_type = pieces[0]
        if self.ins_type == "cpy":
            self.impact_register = pieces[2]
            if pieces[1].isdigit():
                self.literal = True
                self.literal_val = int(pieces[1])
            else:
                self.literal = False
                self.from_register = pieces[1]
                registers[pieces[1]] = 0
        elif self.ins_type == "jnz":
            if pieces[1].isdigit():
                self.literal = True
                self.literal_val = int(pieces[1])
            else:
                self.literal = False
                self.from_register = pieces[1]
                registers[pieces[1]] = 0
            self.adjust = int(pieces[2])
        else:
            self.impact_register = pieces[1]
            registers[pieces[1]] = 0

    def execute(self, ins_index: int, registers: dict[str,int]) -> int:
        """execute instruction"""
        if self.ins_type == "cpy":
            self.copy(registers)
        elif self.ins_type == "inc":
            self.increment(registers)
        elif self.ins_type == "dec":
            self.decrement(registers)
        else:
            return self.jump(registers, ins_index)
        return ins_index + 1

    def copy(self, registers: dict[str,int]):
        """copy instruction"""
        if self.literal:
            registers[self.impact_register] = self.literal_val
        else:
            registers[self.impact_register] = registers[self.from_register]

    def increment(self, registers: dict[str,int]):
        """increment instruction"""
        registers[self.impact_register] = registers[self.impact_register] + 1

    def decrement(self, registers: dict[str,int]):
        """decrement instruction"""
        registers[self.impact_register] = registers[self.impact_register] - 1

    def jump(self, registers: dict[str,int], ins_index: int) -> int:
        """jump instruction"""
        r = 0
        if self.literal:
            r = self.literal_val
        else:
            r = registers[self.from_register]
        if r == 0:
            return ins_index + 1
        return ins_index + self.adjust

def parse_instructions(lines: list[str], registers: dict[str,int]) -> list[Instruction]:
    """parse instructions from input"""
    instructions = []
    for line in lines:
        instructions.append(Instruction(line, registers))
    return instructions

# Data
data = read_lines("input/day12/input.txt")
sample = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a""".splitlines()

# Part 1
#assert solve_part1(sample) == 42
assert solve_part1(data) == 318007

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
