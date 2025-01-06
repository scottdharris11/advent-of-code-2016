"""utility imports"""
import functools
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 13", "Part 1")
def solve_part1(designer: int, goal: tuple[int,int]) -> int:
    """part 1 solving function"""
    ms = MazeSearcher(designer, goal)
    s = Search(ms)
    solution = s.best(SearchMove(0, ms.start))
    if solution is None:
        return -1
    return solution.cost

@runner("Day 13", "Part 2")
def solve_part2(designer: int) -> int:
    """part 2 solving function"""
    check_locs = potential_locations((1,1), 50, designer)
    reachable = 0
    for loc in check_locs:
        ms = MazeSearcher(designer, loc)
        s = Search(ms)
        s.cost_constraint = 50
        solution = s.best(SearchMove(0, ms.start))
        if solution is not None:
            reachable += 1
    return reachable

def potential_locations(start: tuple[int,int], steps: int, designer: int) -> set[tuple[int,int]]:
    """find potential locations to check"""
    locs = set()
    ymin = max(start[1]-steps, 0)
    ymax = start[1]+steps
    for y in range(ymin, ymax+1):
        xsteps = steps - abs(start[0]-y)
        xmin = max(start[0]-xsteps, 0)
        xmax = start[0]+xsteps
        for x in range(xmin, xmax+1):
            loc = (x, y)
            if not wall(loc, designer):
                locs.add(loc)
    return locs

@functools.cache
def wall(coords: tuple[int,int], designer: int) -> bool:
    """determine if supplied coordinate is a wall for the designer"""
    x, y = coords
    num = x*x + 3*x + 2*x*y + y + y*y + designer
    setbits = 0
    while num:
        num &= (num - 1)
        setbits += 1
    return setbits % 2 == 1

class MazeSearcher(Searcher):
    """path search implementation for the maze"""
    def __init__(self, designer: int, goal: tuple[int,int]) -> None:
        self.start = (1,1)
        self.designer = designer
        self.goal = goal

    def is_goal(self, obj: tuple[int,int]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj == self.goal

    def possible_moves(self, obj: tuple[int,int]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in [(1,0),(-1,0),(0,1),(0,-1)]:
            loc = (obj[0] + m[0], obj[1] + m[1])
            if loc[0] < 0 or loc[1] < 0:
                continue
            if wall(loc, self.designer):
                continue
            moves.append(SearchMove(1,loc))
        return moves

    def distance_from_goal(self, obj: tuple[int,int]) -> int:
        """calculate distance from the goal"""
        return abs(self.goal[0]-obj[0]) + abs(self.goal[1]-obj[1])

# Part 1
assert solve_part1(10, (7,4)) == 11
assert solve_part1(1362, (31,39)) == 82

# Part 2
assert solve_part2(1362) == 138
