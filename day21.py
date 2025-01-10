"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(lines: list[str], start: str) -> str:
    """part 1 solving function"""
    rules = parse_rules(lines)
    out = start
    for rule in rules:
        out = rule.apply(out)
    return out

@runner("Day 21", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0


SWAP_POS_MATCH = re.compile(r"swap position ([\d]+) with position ([\d]+)")
SWAP_LETTER_MATCH = re.compile(r"swap letter ([a-z]) with letter ([a-z])")
ROTATE_LEFT_RIGHT = re.compile(r"rotate (left|right) ([\d]+) step[s]?")
ROTATE_BY_LETTER_MATCH = re.compile(r"rotate based on position of letter ([a-z])")
REVERSE_MATCH = re.compile(r"reverse positions ([\d]+) through ([\d]+)")
MOVE_MATCH = re.compile(r"move position ([\d]+) to position ([\d]+)")

class Rule:
    """base rule definition"""
    def apply(self, s) -> str:
        """apply the rule to the supplied string"""
        return s

class SwapPosition(Rule):
    """swap position rule definition"""
    def __init__(self, match: re.Match):
        self.from_pos = int(match.group(1))
        self.to_pos = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        minp = min(self.to_pos, self.from_pos)
        maxp = max(self.to_pos, self.from_pos)
        return "".join([s[0:minp],s[maxp:maxp+1],s[minp+1:maxp],s[minp:minp+1],s[maxp+1:]])

class SwapLetter(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match):
        self.from_letter = match.group(1)[0]
        self.to_letter = match.group(2)[0]

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        positions = []
        for i, c in enumerate(s):
            if c in (self.from_letter, self.to_letter):
                positions.append(i)
        minp = min(positions)
        maxp = max(positions)
        return "".join([s[0:minp],s[maxp:maxp+1],s[minp+1:maxp],s[minp:minp+1],s[maxp+1:]])

class RotateByPos(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match):
        self.dir = match.group(1)
        self.steps = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        if self.dir == "left":
            return s[self.steps:] + s[:self.steps]
        pivot = len(s) - self.steps
        return s[pivot:] + s[:pivot]

class RotateByLetter(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match):
        self.letter = match.group(1)

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        idx = s.find(self.letter)
        pivot = len(s) - idx - 1
        if idx >= 4:
            pivot -= 1
        return s[pivot:] + s[:pivot]

class Reverse(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match):
        self.from_pos = int(match.group(1))
        self.to_pos = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        out = s[:self.from_pos]
        for i in range(self.to_pos, self.from_pos-1, -1):
            out += s[i]
        out += s[self.to_pos+1:]
        return out

class Move(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match):
        self.from_pos = int(match.group(1))
        self.to_pos = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        c = s[self.from_pos]
        out = s[:self.from_pos] + s[self.from_pos+1:]
        out = out[:self.to_pos] + c + out[self.to_pos:]
        return out

def parse_rule(line: str) -> Rule:
    """Parse rule"""
    rules = [
        (SWAP_POS_MATCH, SwapPosition),
        (SWAP_LETTER_MATCH, SwapLetter),
        (ROTATE_LEFT_RIGHT, RotateByPos),
        (ROTATE_BY_LETTER_MATCH, RotateByLetter),
        (REVERSE_MATCH, Reverse),
        (MOVE_MATCH, Move)
    ]

    for rule in rules:
        mr, r = rule
        match = mr.match(line)
        if match is not None:
            return r(match)
    raise ValueError("no rule match")

def parse_rules(lines: list[str]) -> list[Rule]:
    """parse rules from the lines"""
    rules = []
    for line in lines:
        rules.append(parse_rule(line))
    return rules

# Data
data = read_lines("input/day21/input.txt")
sample = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""".splitlines()

# Rule tests
test_rule = parse_rule("swap position 4 with position 0")
assert test_rule.apply("abcde") == "ebcda"
test_rule = parse_rule("swap letter d with letter b")
assert test_rule.apply("ebcda") == "edcba"
test_rule = parse_rule("rotate left 1 step")
assert test_rule.apply("abcde") == "bcdea"
test_rule = parse_rule("rotate right 2 steps")
assert test_rule.apply("abcde") == "deabc"
test_rule = parse_rule("rotate based on position of letter b")
assert test_rule.apply("abdec") == "ecabd"
test_rule = parse_rule("rotate based on position of letter d")
assert test_rule.apply("ecabd") == "decab"
test_rule = parse_rule("reverse positions 0 through 4")
assert test_rule.apply("edcba") == "abcde"
test_rule = parse_rule("move position 1 to position 4")
assert test_rule.apply("bcdea") == "bdeac"
test_rule = parse_rule("move position 3 to position 0")
assert test_rule.apply("bdeac") == "abdec"

# Part 1
assert solve_part1(sample, "abcde") == "decab"
assert solve_part1(data, "abcdefgh") == "gfdhebac"

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
