"""utility imports"""
import hashlib
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 17", "Part 1")
def solve_part1(key: str) -> str:
    """part 1 solving function"""
    vs = VaultSearcher(key)
    s = Search(vs)
    solution = s.best(SearchMove(0, vs.start))
    if solution is None:
        return ""
    return solution.path[-1][1]

@runner("Day 17", "Part 2")
def solve_part2(key: str) -> int:
    """part 2 solving function"""
    vs = VaultSearcher(key)
    return longest_path(vs)

MOVES = "UDLR"

class VaultSearcher(Searcher):
    """path search implementation for the maze"""
    def __init__(self, key: str) -> None:
        self.width = 4
        self.height = 4
        self.start = ((0,0),"")
        self.goal = (3,3)
        self.key = key

    def is_goal(self, obj: tuple[tuple[int,int],str]) -> bool:
        """determine if the supplied state is the goal location"""
        return obj[0] == self.goal

    def possible_moves(self, obj: tuple[tuple[int,int],str]) -> list[SearchMove]:
        """determine possible moves from curent location"""
        pos, path = obj
        moves = []
        k = self.key + path
        copen = hashlib.md5(k.encode()).hexdigest()
        for i, m in enumerate([(0,-1),(0,1),(-1,0),(1,0)]):
            loc = (pos[0] + m[0], pos[1] + m[1])
            if loc[0] < 0 or loc[0] >= self.width or loc[1] < 0 or loc[1] >= self.height:
                continue
            if copen[i] not in "bcdef":
                continue
            moves.append(SearchMove(1,(loc,path + MOVES[i])))
        return moves

    def distance_from_goal(self, obj: tuple[tuple[int,int],str]) -> int:
        """calculate distance from the goal"""
        pos, _ = obj
        return abs(self.goal[0]-pos[0]) + abs(self.goal[1]-pos[1])

def longest_path(vs: VaultSearcher) -> int:
    """find the longest path"""
    queue = []
    queue.append(vs.start)
    maxpath = -1
    while len(queue) > 0:
        cur = queue.pop(-1)
        if vs.is_goal(cur):
            pl = len(cur[1])
            if maxpath == -1 or pl > maxpath:
                maxpath = pl
            continue
        moves = vs.possible_moves(cur)
        for move in moves:
            queue.append(move.state)
    return maxpath

# Part 1
assert solve_part1("ihgpwlah") == "DDRRRD"
assert solve_part1("kglvqrro") == "DDUDRLRRUDRD"
assert solve_part1("ulqzkmiv") == "DRURDRUDDLLDLUURRDULRLDUUDDDRR"
assert solve_part1("gdjjyniy") == "DUDDRLRRRD"

# Part 2
assert solve_part2("ihgpwlah") == 370
assert solve_part2("kglvqrro") == 492
assert solve_part2("ulqzkmiv") == 830
assert solve_part2("gdjjyniy") == 578
