"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    ds = DuctSearcher(lines)
    s = Search(ds)
    
    # compute best routes between all locations
    locations = list(ds.locations.keys())
    locations.sort()
    best_routes = {}
    for i, f in enumerate(locations):
        for t in locations[i+1:]:
            start = (ds.locations[t], ds.locations[f])
            solution = s.best(SearchMove(0, start))
            if solution is None:
                return -1
            best_routes[f+t] = solution.cost
            best_routes[t+f] = solution.cost
    
    # look at each potential location paths for best route
    paths = []
    potential_paths(locations[1:], "", paths)
    best = -1
    for path in paths:
        f = '0'
        steps = 0
        for t in path:
            steps += best_routes[f+t]
            f = t
        if best == -1 or steps < best:
            best = steps
    return best

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

class DuctSearcher(Searcher):
    """search implementation for the storage migrations"""
    def __init__(self, lines: list[str]) -> None:
        self.walls = set()
        self.locations = {}
        for y, row in enumerate(lines):
            for x, col in enumerate(row):
                loc = (x,y)
                if col == '#':
                    self.walls.add(loc)
                elif col != '.':
                    self.locations[col] = loc

    def is_goal(self, obj: tuple[tuple[int,int], tuple[int,int]]) -> bool:
        """determine if the supplied state is the goal"""
        return obj[0] == obj[1]

    def possible_moves(self, obj: tuple[tuple[int,int], tuple[int,int]]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        goal, current = obj
        x, y = current
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            nloc = (x + m[0], y + m[1])
            if nloc in self.walls:
                continue
            moves.append(SearchMove(1, (goal, nloc)))
        return moves

    def distance_from_goal(self, obj: tuple[tuple[int,int], tuple[int,int]]) -> int:
        """calculate distance from the goal"""
        return abs(obj[0][0] - obj[1][0]) + abs(obj[0][1] - obj[1][1])

def potential_paths(locations: list[str], path: str, paths: list[str]) -> None:
    """build set of potential paths based on the set of locations"""
    if len(locations) == 0:
        paths.append(path)
    for l in locations:
        nlocs = list(locations)
        nlocs.remove(l)
        potential_paths(nlocs, path + l, paths)

# Data
data = read_lines("input/day24/input.txt")
sample = """###########
#0.1.....2#
#.#######.#
#4.......3#
###########""".splitlines()

# Part 1
assert solve_part1(sample) == 14
assert solve_part1(data) == 412

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
