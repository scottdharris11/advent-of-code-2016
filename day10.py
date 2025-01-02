"""utility imports"""
import re
from utilities.data import read_lines
from utilities.runner import runner

bot_parse = re.compile(r"bot ([\d]+) gives low to (bot|output) ([\d]+) and high to (bot|output) ([\d]+)")
val_parse = re.compile(r"value ([\d]+) goes to bot ([\d]+)")

@runner("Day 10", "Part 1")
def solve_part1(lines: list[str], goal: tuple[int,int]) -> int:
    """part 1 solving function"""
    bots = parse_bots(lines, goal)
    run_bots(bots)
    for bot in bots.values():
        if bot.goal_bot:
            return bot.bot_id
    return -1

@runner("Day 10", "Part 2")
def solve_part2(lines: list[str], goal: tuple[int,int]) -> int:
    """part 2 solving function"""
    bots = parse_bots(lines, goal)
    outputs = run_bots(bots)
    return outputs[0] * outputs[1] * outputs[2]

class Bot:
    """structure and functions of a bot"""
    def __init__(self, bot_id: int, goal: tuple[int,int]):
        self.bot_id = bot_id
        self.chip1 = None
        self.chip2 = None
        self.low = ("",0)
        self.high = ("",0)
        self.goal = goal
        self.goal_bot = False

    def ready_to_work(self) -> bool:
        """determine if bot is ready to work"""
        return self.chip1 is not None and self.chip2 is not None

    def take_chip(self, chip: int):
        """take a chip into input"""
        if self.chip1 is None:
            self.chip1 = chip
        else:
            self.chip2 = chip
            if self.is_goal_bot(self.goal[0], self.goal[1]):
                self.goal_bot = True

    def is_goal_bot(self, a: int, b: int) -> bool:
        """determine if bot handles goal chip values"""
        return (a == self.chip1 and b == self.chip2) or (b == self.chip1 and a == self.chip2)

    def work(self, bots: dict[int,any], outputs: dict[int,int]):
        """perform work based on instructions"""
        if not self.ready_to_work():
            return
        lowval = min(self.chip1, self.chip2)
        if self.low[0] == "bot":
            bots[self.low[1]].take_chip(lowval)
        else:
            outputs[self.low[1]] = lowval
        highval = max(self.chip1, self.chip2)
        if self.high[0] == "bot":
            bots[self.high[1]].take_chip(highval)
        else:
            outputs[self.high[1]] = highval
        self.chip1 = None
        self.chip2 = None

def parse_bots(lines: list[str], goal: tuple[int,int]) -> dict[int,Bot]:
    """parse and initialize bots with supplied instructions"""
    bots = {}
    for line in lines:
        if line.startswith("value"):
            continue
        m = bot_parse.match(line)
        bot = Bot(int(m.group(1)), goal)
        bot.low = (m.group(2), int(m.group(3)))
        bot.high = (m.group(4), int(m.group(5)))
        bots[bot.bot_id] = bot

    for line in lines:
        if not line.startswith("value"):
            continue
        m = val_parse.match(line)
        bot = int(m.group(2))
        chip = int(m.group(1))
        bots[bot].take_chip(chip)
    return bots

def run_bots(bots: dict[int,Bot]) -> dict[int,int]:
    """run the bots until no more work"""
    outputs = {}
    while True:
        for bot in bots.values():
            bot.work(bots, outputs)
        for bot in bots.values():
            if bot.ready_to_work():
                break
        else:
            break
    return outputs

# Data
data = read_lines("input/day10/input.txt")
sample = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2""".splitlines()

# Part 1
assert solve_part1(sample, (2, 5)) == 2
assert solve_part1(data, (61, 17)) == 116

# Part 2
assert solve_part2(sample, (2, 5)) == 30
assert solve_part2(data, (61, 17)) == 23903
