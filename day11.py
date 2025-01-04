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
    fps = FacilityPathSearcher(lines)
    fps.start.pairs.append((1,1))
    fps.start.pairs.append((1,1))
    s = Search(fps)
    solution = s.best(SearchMove(0, fps.start))
    if solution is None:
        return -1
    return solution.cost

def parse_items(item_type: str, line: str) -> set[str]:
    """parse out items of a particular type from the supplied string"""
    items = set()
    idx = line.find(item_type)
    while idx >= 0:
        bidx = idx-2
        while True:
            if line[bidx] == ' ':
                break
            bidx -= 1
        items.add(line[bidx+1:idx-1])
        idx = line.find(item_type, idx + len(item_type))
    return items

def valid_state(pairs: list[tuple[int,int]]) -> bool:
    """check to see if the state is valid"""
    # for each floor, valid if:
    #   - no microchips
    #   - no generators
    #   - any microchip has matching generator
    for f in range(1,5):
        chip_cnt = 0
        gen_cnt = 0
        chip_nogen = False
        for chip, gen in pairs:
            chip_cnt = chip_cnt + 1 if chip == f else chip_cnt
            gen_cnt = gen_cnt + 1 if gen == f else gen_cnt
            chip_nogen = True if chip == f and gen !=f else chip_nogen
        if chip_cnt == 0 or gen_cnt == 0:
            continue
        if gen_cnt > 0 and chip_nogen:
            return False
    return True

class FacilityState:
    """represent the current facility state"""
    def __init__(self, floor: int, pairs: list[tuple[int,int]]):
        self.floor = floor
        self.pairs = sorted(pairs)

    def __repr__(self):
        return str((self.floor, self.pairs))

    def __hash__(self) -> int:
        return hash((self.floor, tuple(self.pairs)))

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if self.floor != other.floor:
            return False
        if self.pairs != other.pairs:
            return False
        return True

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def is_goal(self) -> bool:
        """determine if the supplied state is the goal (everything on 4th floor)"""
        if self.floor != 4:
            return False
        for chip, gen in self.pairs:
            if chip != 4 or gen != 4:
                return False
        return True

    def possible_moves(self) -> list:
        """determine possible moves from curent location"""
        possible = []
        possible.extend(self.moves_to_floor(self.floor+1))
        possible.extend(self.moves_to_floor(self.floor-1))
        return possible

    def moves_to_floor(self, to: int) -> list:
        """build possible move states from current to the supplied floor"""
        if to > 4 or to < 1:
            return []

        # find all indexes active on the floor, when pair on
        # same floor, see if we can move them together
        moves = set()
        chips = []
        gens = []
        for idx, pair in enumerate(self.pairs):
            chip, gen = pair
            if chip == self.floor:
                chips.append(idx)
            if gen == self.floor:
                gens.append(idx)
            if chip == self.floor and gen == self.floor:
                npairs = list(self.pairs)
                npairs[idx] = (to, to)
                if valid_state(npairs):
                    moves.add(FacilityState(to, npairs))

        # all chips independently and combined
        for i, ca in enumerate(chips):
            npairs = list(self.pairs)
            _, cgen = npairs[ca]
            npairs[ca] = (to, cgen)
            if valid_state(npairs):
                moves.add(FacilityState(to, npairs))
            for _, cb in enumerate(chips, i):
                npairs = list(self.pairs)
                _, cgen = npairs[ca]
                npairs[ca] = (to, cgen)
                _, cgen = npairs[cb]
                npairs[cb] = (to, cgen)
                if valid_state(npairs):
                    moves.add(FacilityState(to, npairs))

        # all generators independently and combined
        for i, ga in enumerate(gens):
            npairs = list(self.pairs)
            cchip, _ = npairs[ga]
            npairs[ga] = (cchip, to)
            if valid_state(npairs):
                moves.add(FacilityState(to, npairs))
            for _, gb in enumerate(gens, i):
                npairs = list(self.pairs)
                cchip, _ = npairs[ga]
                npairs[ga] = (cchip, to)
                cchip, _ = npairs[gb]
                npairs[gb] = (cchip, to)
                if valid_state(npairs):
                    moves.add(FacilityState(to, npairs))

        # all valid chip/generator combinations
        for chip in chips:
            for gen in gens:
                npairs = list(self.pairs)
                _, cgen = npairs[chip]
                npairs[chip] = (to, cgen)
                cchip, _ = npairs[gen]
                npairs[gen] = (cchip, to)
                if valid_state(npairs):
                    moves.add(FacilityState(to, npairs))
        return moves

class FacilityPathSearcher(Searcher):
    """path search implementation for the facility"""
    def __init__(self, lines: list[str]) -> None:
        generators = {}
        chips = {}
        for f, line in enumerate(lines):
            for gen in parse_items("generator", line):
                generators[gen] = f+1
            for chip in parse_items("microchip", line):
                chips[chip] = f+1
        pairs = []
        for gen, floor in generators.items():
            chip_floor = chips[gen+"-compatible"]
            pairs.append((chip_floor, floor))
        self.start = FacilityState(1, pairs)

    def is_goal(self, obj: FacilityState) -> bool:
        """determine if the supplied state is the goal (everything on 4th floor)"""
        return obj.is_goal()

    def possible_moves(self, obj: FacilityState) -> list[SearchMove]:
        """determine possible moves from curent location"""
        moves = []
        for m in obj.possible_moves():
            moves.append(SearchMove(1,m))
        return moves

    def distance_from_goal(self, obj: FacilityState) -> int:
        """calculate distance from the goal"""
        d = 0
        for p in obj.pairs:
            d += 4-p[0] + 4-p[1]
        return d

# Data
data = read_lines("input/day11/input.txt")
sample = \
"""The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""".splitlines()

# Part 1
assert solve_part1(sample) == 11
assert solve_part1(data) == 47

# Part 2
assert solve_part2(data) == 71
