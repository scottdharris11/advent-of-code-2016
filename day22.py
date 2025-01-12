"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

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
    nodes = parse_nodes(lines)
    sms = StorageMoveSearcher(nodes)
    s = Search(sms)
    solution = s.best(SearchMove(0, sms.start))
    if solution is None:
        return -1
    return solution.cost

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

class StorageState:
    """storage state definition"""
    def __init__(self, mdata: tuple[int,int], fdata: tuple[int,int]):
        self.memory_loc = mdata
        self.free_loc = fdata

    def __repr__(self):
        return str((self.memory_loc, self.free_loc))

    def __hash__(self) -> int:
        return hash((self.memory_loc, self.free_loc))

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self.memory_loc != other.memory_loc:
            return False
        if self.free_loc != other.free_loc:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

class StorageMoveSearcher(Searcher):
    """search implementation for the storage migrations"""
    def __init__(self, nodes: list[Node]) -> None:
        max_x = -1
        max_y = -1
        free_max = 0
        nodes_by_loc = {}
        for node in nodes:
            if max_x == -1 or node.loc[0] > max_x:
                max_x = node.loc[0]
            if max_y == -1 or node.loc[1] > max_y:
                max_y = node.loc[1]
            nodes_by_loc[node.loc] = node
            if node.used == 0:
                free_max = node.size
        self.height = max_y + 1
        self.width = max_x + 1
        self.grid = []
        free = None
        for y in range(self.height):
            row = []
            for x in range(self.width):
                node = nodes_by_loc[(x,y)]
                if node.used > free_max:
                    row.append('#')
                else:
                    row.append('.')
                    if node.used == 0:
                        free = (x, y)
            self.grid.append(row)
        self.start = StorageState((max_x,0), free)
        self.goal = (0,0)

    def is_goal(self, obj: StorageState) -> bool:
        """determine if the supplied state is the goal (goal storage at goal location)"""
        return obj.memory_loc == self.goal

    def possible_moves(self, obj: StorageState) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        x, y = obj.free_loc
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            to_x = x + m[0]
            to_y = y + m[1]
            if to_x < 0 or to_x >= self.width or to_y < 0 or to_y >= self.height:
                continue
            if self.grid[to_y][to_x] == '#':
                continue
            mloc = (x, y) if (to_x, to_y) == obj.memory_loc else obj.memory_loc
            moves.append(SearchMove(1, StorageState(mloc, (to_x, to_y))))
        return moves

    def distance_from_goal(self, obj: StorageState) -> int:
        """calculate distance from the goal"""
        memx, memy = obj.memory_loc
        goalx, goaly = self.goal
        freex, freey = obj.free_loc
        d = abs(memx - goalx) + abs(memy - goaly)
        d += (abs(memx - freex) + abs(memy - freey)) * 10
        return d

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
sample = """root@ebhq-gridcenter# df -h
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""".splitlines()

# Part 1
assert solve_part1(data) == 901

# Part 2
assert solve_part2(sample) == 7
assert solve_part2(data) == 238
