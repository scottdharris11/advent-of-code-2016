"""Module providing a-star search implementation"""

class PriorityQueue:
    """queue ordered by priority value"""
    def __init__(self) -> None:
        self.items = []
        self.size = 0

    def empty(self) -> bool:
        """determines if queue is empty"""
        return self.size == 0

    def next(self) -> any:
        """dequeue the next value"""
        n = self.size - 1
        item = self.items[n]
        self.items = self.items[:n]
        self.size -= 1
        return item[0]

    def queue(self, obj: any, priority: int):
        """place value in the queue based on priority"""
        qi = (obj, priority)

        idx = -1
        for i, item in enumerate(self.items):
            if item[1] < priority:
                idx = i
                break

        if idx == -1:
            self.items.append(qi)
        else:
            self.items.insert(idx, qi)
        self.size += 1

class SearchMove:
    """encapsulates the cost and state of a move"""
    def __init__(self, cost: int, state) -> None:
        self.cost = cost
        self.state = state

    def __repr__(self) -> str:
        return str((self.cost, self.state))

class Searcher:
    """base search plugin implementation"""
    # pylint: disable=unused-argument
    def is_goal(self, obj) -> bool:
        """returns True when goal of search is met"""
        return True

    def possible_moves(self, obj) -> list[SearchMove]:
        """returns the possible moves from the current state"""
        return []

    def distance_from_goal(self, obj) -> int:
        """returns a distance from current state to goal"""
        return 0

class SearchSolution:
    """represents the shortest path and cost found"""
    def __init__(self, cost: int, path) -> None:
        self.cost = cost
        self.path = path

    def __repr__(self) -> str:
        return str((self.cost, self.path))

class Search:
    """search implementation"""
    def __init__(self, searcher: Searcher) -> None:
        self.searcher = searcher
        self.cost_constraint = 0

    # utilize a-star search approach to find the path to the goal
    # with the lowest cost.
    def best(self, init: SearchMove) -> SearchSolution:
        """find best path from the initial move"""
        q = PriorityQueue()
        q.queue(init.state, init.cost)
        cost = {init.state: init.cost}
        from_state = {}
        goal = None
        while not q.empty():
            current = q.next()
            if self.searcher.is_goal(current):
                goal = current
                break

            for move in self.searcher.possible_moves(current):
                new_cost = cost[current] + move.cost
                if self.cost_constraint > 0 and new_cost > self.cost_constraint:
                    continue
                current_cost = cost.get(move.state, -1)
                if current_cost == -1 or new_cost < current_cost:
                    cost[move.state] = new_cost
                    priority = new_cost + self.searcher.distance_from_goal(move.state)
                    q.queue(move.state, priority)
                    from_state[move.state] = current

        if goal is None:
            return None

        path = [goal]
        current = goal
        while current != init.state:
            current = from_state[current]
            path.insert(0, current)

        return SearchSolution(cost[goal], path)
