"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 22", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    nodes = parse_nodes(lines)
    viable = 0
    for x, node_a in enumerate(nodes):
        for _, node_b in enumerate(nodes[x+1:]):
            if viable_pair(node_a, node_b):
                viable += 1
            if viable_pair(node_b, node_a):
                viable += 1
    return viable

@runner("Day 22", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class Node:
    """storage node definition"""
    def __init__(self, line: str):
        self.name, size, used, avail, _ = line.split()
        _, x, y = self.name.split("-")
        self.loc = (int(x[1:]), int(y[1:]))
        self.size = int(size[:-1])
        self.used = int(used[:-1])
        self.avail = int(avail[:-1])

    def __repr__(self):
        return str((self.name, self.loc, self.size, self.used, self.avail))

def viable_pair(a: Node, b: Node) -> bool:
    """determine if pair is viable"""
    if a.used == 0:
        return False
    if a.name == b.name:
        return False
    return a.used <= b.avail

def parse_nodes(lines: list[str]) -> list[Node]:
    """parse nodes from the input"""
    nodes = []
    for line in lines[2:]:
        nodes.append(Node(line))
    return nodes

# Data
data = read_lines("input/day22/input.txt")

# Part 1
assert solve_part1(data) == 901

# Part 2
assert solve_part2(data) == 0
