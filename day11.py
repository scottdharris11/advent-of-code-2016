"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner
from utilities.search import Search, Searcher, SearchMove

@runner("Day 11", "Part 1")
def solve_part1(lines: list[str]) -> int:
    """part 1 solving function"""
    fps = FacilityPathSearcher(lines)
    s = Search(fps)
    solution = s.best(SearchMove(0, fps.start))
    if solution is None:
        return -1
    return solution.cost

@runner("Day 11", "Part 2")
def solve_part2(lines: list[str]) -> int:
    """part 2 solving function"""
    return 0

def parse_items(item_type: str, line: str) -> list[str]:
    """parse out items of a particular type from the supplied string"""
    items = []
    idx = line.find(item_type)
    while idx >= 0:
        bidx = idx-2
        while True:
            if line[bidx] == ' ':
                break
            bidx -= 1
        items.append(line[bidx+1:idx-1])
        idx = line.find(item_type, idx + len(item_type))
    return items

def newlist_append(l: list[str], item: str) -> list[str]:
    """build new list with supplied item appended"""
    nlist = list(l)
    nlist.append(item)
    return nlist

def newlist_remove(l: list[str], item: str) -> list[str]:
    """build new list with supplied item removed"""
    nlist = list(l)
    nlist.remove(item)
    return nlist

class FacilityState:
    """represent the current facility state"""
    def __init__(self, floor: int, generators: dict[int,list[str]], chips: dict[int,list[str]]):
        self.floor = floor
        self.generators = {}
        for f, items in generators.items():
            self.generators[f] = sorted(items)
        self.chips = {}
        for f, items in chips.items():
            self.chips[f] = sorted(items)

    def __repr__(self):
        return str((self.floor, self.generators, self.chips))

    def __hash__(self) -> int:
        h = hash(self.floor)
        for f, items in self.generators.items():
            h += hash((f, tuple(items)))
        for f, items in self.chips.items():
            h += hash((f, tuple(items)))
        return h

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self.floor != other.floor:
            return False
        if self.generators != other.generators:
            return False
        if self.chips != other.chips:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def valid(self) -> bool:
        """check to see if the state is valid"""
        # for each floor, valid if:
        #   - no microchips
        #   - no generators
        #   - any microchip has matching generator
        for f in range(1,5):
            if len(self.chips[f]) == 0:
                continue
            if len(self.generators[f]) == 0:
                continue
            for c in self.chips[f]:
                compgen = c.split("-")[0]
                if compgen not in self.generators[f]:
                    return False
        return True

class FacilityPathSearcher(Searcher):
    """path search implementation for the facility"""
    def __init__(self, lines: list[str]) -> None:
        generators = {}
        chips = {}
        for f, line in enumerate(lines):
            generators[f+1] = parse_items("generator", line)
            chips[f+1] = parse_items("microchip", line)
        self.start = FacilityState(1, generators, chips)

    def is_goal(self, obj: FacilityState) -> bool:
        """determine if the supplied state is the goal (everything on 4th floor)"""
        if obj.floor != 4:
            return False
        for f in range(1,4):
            if len(obj.generators[f]) > 0:
                return False
            if len(obj.chips[f]) > 0:
                return False
        return True

    def possible_moves(self, obj: FacilityState) -> list[SearchMove]:
        """determine possible moves from curent location"""
        possible = []
        possible.extend(self.moves_to_floor(obj, obj.floor+1))
        possible.extend(self.moves_to_floor(obj, obj.floor-1))
        return possible

    def moves_to_floor(self, obj: FacilityState, to: int) -> list[SearchMove]:
        """build possible move states from current to the supplied floor"""
        if to > 4 or to < 1:
            return []

        # check each generator and chip individually to see if it can move
        positems = []
        moves = []
        for gen in obj.generators[obj.floor]:
            positems.append(gen)
            ngens = dict(obj.generators)
            ngens[to] = newlist_append(ngens[to], gen)
            ngens[obj.floor] = newlist_remove(ngens[obj.floor], gen)
            nstate = FacilityState(to, ngens, obj.chips)
            if nstate.valid():
                moves.append(SearchMove(1,nstate))
        for chip in obj.chips[obj.floor]:
            positems.append(chip)
            nchips = dict(obj.chips)
            nchips[to] = newlist_append(nchips[to], chip)
            nchips[obj.floor] = newlist_remove(nchips[obj.floor], chip)
            nstate = FacilityState(to, obj.generators, nchips)
            if nstate.valid():
                moves.append(SearchMove(1,nstate))

        # for each item that could move independently, combine them
        # to see if we can move two at a time
        for idxa, itema in enumerate(positems):
            for _, itemb in enumerate(positems[idxa+1:]):
                ngens = dict(obj.generators)
                nchips = dict(obj.chips)
                if itema.find("-") > 0:
                    nchips[to] = newlist_append(nchips[to], itema)
                    nchips[obj.floor] = newlist_remove(nchips[obj.floor], itema)
                else:
                    ngens[to] = newlist_append(ngens[to], itema)
                    ngens[obj.floor] = newlist_remove(ngens[obj.floor], itema)
                if itemb.find("-") > 0:
                    nchips[to] = newlist_append(nchips[to], itemb)
                    nchips[obj.floor] = newlist_remove(nchips[obj.floor], itemb)
                else:
                    ngens[to] = newlist_append(ngens[to], itemb)
                    ngens[obj.floor] = newlist_remove(ngens[obj.floor], itemb)
                nstate = FacilityState(to, ngens, nchips)
                if nstate.valid():
                    moves.append(SearchMove(1,nstate))
        return moves

    def distance_from_goal(self, obj: FacilityState) -> int:
        """calculate distance from the goal"""
        d = 0
        for f in range(1,5):
            fic = len(obj.generators[f]) + len(obj.chips[f])
            d += int(fic / 2) * (4-f+abs(obj.floor - f))
        return d

# Data
data = read_lines("input/day11/input.txt")
sample = """The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".splitlines()

# Part 1
assert solve_part1(sample) == 11
assert solve_part1(data) == 47

# Part 2
assert solve_part2(sample) == 0
assert solve_part2(data) == 0
