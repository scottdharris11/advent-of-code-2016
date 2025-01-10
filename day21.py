"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 21", "Part 1")
def solve_part1(lines: list[str], start: str) -> str:
    """part 1 solving function"""
    rules = parse_rules(lines, False)
    out = start
    for rule in rules:
        out = rule.apply(out)
    return out

@runner("Day 21", "Part 2")
def solve_part2(lines: list[str], start: str) -> str:
    """part 2 solving function"""
    rules = parse_rules(lines, True)
    rules.reverse()
    out = start
    for rule in rules:
        out = rule.apply(out)
    return out

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
    def __init__(self, match: re.Match, _: bool):
        self.pos1 = int(match.group(1))
        self.pos2 = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        minp = min(self.pos2, self.pos1)
        maxp = max(self.pos2, self.pos1)
        return "".join([s[0:minp],s[maxp:maxp+1],s[minp+1:maxp],s[minp:minp+1],s[maxp+1:]])

class SwapLetter(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match, _: bool):
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
    def __init__(self, match: re.Match, reverse: bool):
        self.dir = match.group(1)
        if reverse:
            self.dir = "left" if self.dir == "right" else "right"
        self.steps = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        pivot = self.steps
        if self.dir == "right":
            pivot = len(s) - self.steps
        return s[pivot:] + s[:pivot]

class RotateByLetter(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match, reverse: bool):
        self.letter = match.group(1)
        self.reverse = reverse

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        idx = s.find(self.letter)
        length = len(s)
        if self.reverse:
            # how can we do this without mapping
            # idx 1 -> pivot 1
            # idx 3 -> pivot 2
            # idx 5 -> pivot 3
            # idx 7 -> pivot 4
            # idx 2 -> pivot 6
            # idx 4 -> pivot 7
            # idx 6 -> pivot 0
            # idx 0 -> pivot 1
            rp = {1:1, 3:2, 5:3, 7:4, 2:6, 4:7, 6:0, 0:1}
            pivot = rp[idx]
        else:
            steps = idx + 1
            if idx >= 4:
                steps += 1
            pivot = length - (steps % length)
        return s[pivot:] + s[:pivot]

class Reverse(Rule):
    """swap letter rule definition"""
    def __init__(self, match: re.Match, _: bool):
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
    def __init__(self, match: re.Match, reverse: bool):
        if reverse:
            self.from_pos = int(match.group(2))
            self.to_pos = int(match.group(1))
        else:
            self.from_pos = int(match.group(1))
            self.to_pos = int(match.group(2))

    def apply(self, s: str) -> str:
        """apply the rule to the supplied string"""
        c = s[self.from_pos]
        out = s[:self.from_pos] + s[self.from_pos+1:]
        out = out[:self.to_pos] + c + out[self.to_pos:]
        return out

def parse_rule(line: str, reverse: bool) -> Rule:
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
            return r(match, reverse)
    raise ValueError("no rule match")

def parse_rules(lines: list[str], reverse: bool) -> list[Rule]:
    """parse rules from the lines"""
    rules = []
    for line in lines:
        rules.append(parse_rule(line, reverse))
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
test_rule = parse_rule("swap position 4 with position 0", False)
assert test_rule.apply("abcde") == "ebcda"
test_rule = parse_rule("swap position 4 with position 0", True)
assert test_rule.apply("ebcda") == "abcde"

test_rule = parse_rule("swap letter d with letter b", False)
assert test_rule.apply("ebcda") == "edcba"
test_rule = parse_rule("swap letter d with letter b", True)
assert test_rule.apply("edcba") == "ebcda"

test_rule = parse_rule("rotate left 1 step", False)
assert test_rule.apply("abcde") == "bcdea"
test_rule = parse_rule("rotate left 1 step", True)
assert test_rule.apply("bcdea") == "abcde"
test_rule = parse_rule("rotate right 2 steps", False)
assert test_rule.apply("abcde") == "deabc"
test_rule = parse_rule("rotate right 2 steps", True)
assert test_rule.apply("deabc") == "abcde"

test_rule = parse_rule("rotate based on position of letter b", False)
assert test_rule.apply("abdec") == "ecabd"
test_rule = parse_rule("rotate based on position of letter d", False)
assert test_rule.apply("ecabd") == "decab"

TEST_STRING = "abcdefgh"
for test_c in TEST_STRING:
    test_rule_text = "rotate based on position of letter " + test_c
    test_rule = parse_rule(test_rule_text, False)
    test_out = test_rule.apply(TEST_STRING)
    test_rule = parse_rule(test_rule_text, True)
    reverse_out = test_rule.apply(test_out)
    #print((test_c, test_string, test_out, reverse_out))
    assert reverse_out == TEST_STRING

test_rule = parse_rule("reverse positions 0 through 4", False)
assert test_rule.apply("edcba") == "abcde"
test_rule = parse_rule("reverse positions 0 through 4", True)
assert test_rule.apply("abcde") == "edcba"

test_rule = parse_rule("move position 1 to position 4", False)
assert test_rule.apply("bcdea") == "bdeac"
test_rule = parse_rule("move position 1 to position 4", True)
assert test_rule.apply("bdeac") == "bcdea"
test_rule = parse_rule("move position 3 to position 0", False)
assert test_rule.apply("bdeac") == "abdec"
test_rule = parse_rule("move position 3 to position 0", True)
assert test_rule.apply("abdec") == "bdeac"

# Part 1
assert solve_part1(sample, "abcde") == "decab"
assert solve_part1(data, "abcdefgh") == "gfdhebac"

# Part 2
assert solve_part2(sample, "decab") == "abcde"
assert solve_part2(data, "fbgdceah") == "dhaegfbc"
