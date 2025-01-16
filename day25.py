"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 25", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    a = 0
    while True:
        #print("running with a == " + str(a))
        out = run_program(lines, a)
        #print(out)
        if out == "0101010101":
            break
        a += 1
    return a

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

    def execute(self, ins_index: int, registers: dict[str,int]) -> int:
        """execute instruction"""
        if self.ins_type == "cpy":
            self.copy(registers)
        elif self.ins_type == "inc":
            self.increment(registers)
        elif self.ins_type == "dec":
            self.decrement(registers)
        elif self.ins_type == "out":
            self.out(registers)
        elif self.ins_type == "mul":
            self.multiply(registers)
        elif self.ins_type == "nop":
            pass
        elif self.ins_type == "custom1":
            self.custom1(registers)
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

    def multiply(self, registers: dict[str,int]):
        """multiply instruction"""
        p1 = self.param1_val if self.param1_literal else registers[self.param1_register]
        p2 = self.param2_val if self.param2_literal else registers[self.param2_register]
        registers['d'] = registers['d'] + (p1 * p2)
        #print("multiply, adding to 'a': " + str(p1) + " * " + str(p2))

    def out(self, registers: dict[str,int]):
        """out instruction"""
        p1 = self.param1_val if self.param1_literal else registers[self.param1_register]
        registers['out'] = registers['out'] + str(p1)
        #print("out, adding to 'out': " + str(p1))

    def custom1(self, registers: dict[str,int]):
        """custom function"""
        # a == b / 2 (round down)
        # b == zero
        # c == 2 - (b % 2)
        b = registers['b']
        registers['a'] = b // 2
        registers['b'] = 0
        registers['c'] = 2 - (b % 2)

def parse_instructions(lines: list[str], registers: dict[str,int]) -> list[Instruction]:
    """parse instructions from input"""
    instructions = []
    for line in lines:
        instructions.append(Instruction(line, registers))
    return instructions

def run_program(lines: list[str], a_start: int) -> str:
    """run program with supplied input into register a and return output"""
    registers = {}
    instructions = parse_instructions(lines, registers)
    registers['out'] = ''

    # override main loops and replace with custom ops
    no = Instruction("nop 0", registers)
    instructions[1] = Instruction("mul 4 633", registers)
    instructions[2] = no
    instructions[3] = no
    instructions[4] = no
    instructions[5] = no
    instructions[6] = no
    instructions[7] = no
    instructions[12] = Instruction("custom1 0", registers)
    instructions[13] = no
    instructions[14] = no
    instructions[15] = no
    instructions[16] = no
    instructions[17] = no
    instructions[18] = no
    instructions[19] = no

    registers['a'] = a_start
    max_idx = len(instructions)-1
    idx = 0
    while True:
        #print("executing instruction " + str(idx+1) + ": " + str(registers))
        idx = instructions[idx].execute(idx, registers)
        if idx < 0 or idx > max_idx:
            break
        if len(registers['out']) == 10:
            break
    return registers['out']

# Data
data = read_lines("input/day25/input.txt")

# Part 1
assert solve_part1(data) == 198
