"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 23", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    return run_program(lines, 7)

@runner("Day 23", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return run_program(lines, 12)

def run_program(lines: list[str], a_start: int) -> int:
    """run program with supplied input into register a and return output"""
    registers = {}
    instructions = parse_instructions(lines, registers)
    if len(instructions) > 7:
        # override main loops and replace with multiplication ops
        ni = Instruction("mul c d", registers)
        np = Instruction("nop 0", registers)
        instructions[5] = np
        instructions[6] = np
        instructions[7] = np
        instructions[8] = np
        instructions[9] = ni
        instructions[21] = np
        instructions[22] = np
        instructions[23] = np
        instructions[24] = np
        instructions[25] = ni
    registers['a'] = a_start
    max_idx = len(instructions)-1
    idx = 0
    while True:
        #print("executing instruction " + str(idx+1) + ": " + str(registers))
        idx = instructions[idx].execute(idx, registers, instructions)
        if idx < 0 or idx > max_idx:
            break
    return registers['a']

class Instruction:
    """definition for instruction"""
    def __init__(self, line: str, registers: dict[str,int]):
        pieces = line.split(" ")
        self.ins_type = pieces[0]
        if pieces[1].isdigit() or pieces[1][0] == '-':
            self.param1_literal = True
            self.param1_val = int(pieces[1])
        else:
            self.param1_literal = False
            self.param1_register = pieces[1]
            registers[pieces[1]] = 0
        if self.ins_type in ["cpy", "jnz", "mul"]:
            if pieces[2].isdigit() or pieces[2][0] == '-':
                self.param2_literal = True
                self.param2_val = int(pieces[2])
            else:
                self.param2_literal = False
                self.param2_register = pieces[2]
                registers[pieces[2]] = 0

    def execute(self, ins_index: int, registers: dict[str,int], instructions: list) -> int:
        """execute instruction"""
        if self.ins_type == "cpy":
            self.copy(registers)
        elif self.ins_type == "inc":
            self.increment(registers)
        elif self.ins_type == "dec":
            self.decrement(registers)
        elif self.ins_type == "tgl":
            self.toggle(registers, ins_index, instructions)
        elif self.ins_type == "mul":
            self.multiply(registers)
        elif self.ins_type == "nop":
            pass
        else:
            return self.jump(registers, ins_index)
        return ins_index + 1

    def copy(self, registers: dict[str,int]):
        """copy instruction"""
        if self.param2_literal:
            return
        if self.param1_literal:
            registers[self.param2_register] = self.param1_val
        else:
            registers[self.param2_register] = registers[self.param1_register]

    def increment(self, registers: dict[str,int]):
        """increment instruction"""
        registers[self.param1_register] = registers[self.param1_register] + 1

    def decrement(self, registers: dict[str,int]):
        """decrement instruction"""
        registers[self.param1_register] = registers[self.param1_register] - 1

    def jump(self, registers: dict[str,int], ins_index: int) -> int:
        """jump instruction"""
        r = self.param1_val if self.param1_literal else registers[self.param1_register]
        if r == 0:
            return ins_index + 1
        adjust = self.param2_val if self.param2_literal else registers[self.param2_register]
        #print("jumping, check value: " + str(r) + ", adjust: " + str(adjust))
        return ins_index + adjust

    def toggle(self, registers: dict[str,int], ins_index: int, instructions: list):
        """toggle instruction"""
        adjust = self.param1_val if self.param1_literal else registers[self.param1_register]
        idx = ins_index + adjust
        if idx < 0 or idx >= len(instructions):
            #print("skipping toggle at: " + str(idx))
            return
        ins = instructions[idx]
        if ins.ins_type == "jnz":
            ins.ins_type = "cpy"
        elif ins.ins_type == "cpy":
            ins.ins_type = "jnz"
        elif ins.ins_type == "inc":
            ins.ins_type = "dec"
        elif ins.ins_type in ["dec","tgl"]:
            ins.ins_type = "inc"
        else:
            #raise(ValueError("toggling mutated command: " + str(idx)))
            pass
        #print("toggling instruction at " + str(idx) + ": " + ins.ins_type)

    def multiply(self, registers: dict[str,int]) -> int:
        """multiply instruction"""
        p1 = self.param1_val if self.param1_literal else registers[self.param1_register]
        p2 = self.param2_val if self.param2_literal else registers[self.param2_register]
        registers['a'] = registers['a'] + (p1 * p2)
        #print("multiply, adding to 'a': " + str(p1) + " * " + str(p2))

def parse_instructions(lines: list[str], registers: dict[str,int]) -> list[Instruction]:
    """parse instructions from input"""
    instructions = []
    for line in lines:
        instructions.append(Instruction(line, registers))
    return instructions

# Data
data = read_lines("input/day23/input.txt")
sample = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a""".splitlines()

# Part 1
assert solve_part1(sample) == 3
assert solve_part1(data) == 10661

# Part 2
assert solve_part2(data) == 479007221
