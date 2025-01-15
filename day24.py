"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 24", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    locations, routes = best_routes(lines)
    paths = potential_paths(locations[1:], "", [])
    return best_path(routes, paths, False)

@runner("Day 24", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    locations, routes = best_routes(lines)
    paths = potential_paths(locations[1:], "", [])
    return best_path(routes, paths, True)

class DuctSearcher(Searcher):
    """search implementation for the duct paths"""
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

def best_routes(lines: list[str]) -> tuple[list[str],dict[str,int]]:
    """compute best routes between all locations"""
    ds = DuctSearcher(lines)
    s = Search(ds)
    locations = list(ds.locations.keys())
    locations.sort()
    br = {}
    for i, f in enumerate(locations):
        for t in locations[i+1:]:
            start = (ds.locations[t], ds.locations[f])
            solution = s.best(SearchMove(0, start))
            if solution is None:
                raise ValueError("no path between locations: " + f + "," + t)
            br[f+t] = solution.cost
            br[t+f] = solution.cost
    return locations, br

def potential_paths(locations: list[str], path: str, paths: list[str]) -> list[str]:
    """build set of potential paths based on the set of locations"""
    if len(locations) == 0:
        paths.append(path)
    for l in locations:
        nlocs = list(locations)
        nlocs.remove(l)
        potential_paths(nlocs, path + l, paths)
    return paths

def best_path(routes: dict[str,int], paths: list[str], back_home: bool) -> int:
    """determine the best path (least steps)"""
    best = -1
    for path in paths:
        f = '0'
        steps = 0
        for t in path:
            steps += routes[f+t]
            f = t
        if back_home:
            steps += routes[f+'0']
        if best == -1 or steps < best:
            best = steps
    return best

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
assert solve_part2(sample) == 20
assert solve_part2(data) == 664
