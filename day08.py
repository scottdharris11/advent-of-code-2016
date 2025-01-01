"""utility imports"""
from utilities.data import read_lines
from utilities.runner import runner

@runner("Day 8", "Part 1")
def solve_part1(instructions: list[str], width: int, height: int) -> int:
    """part 1 solving function"""
    grid = []
    for _ in range(height):
        grid.append([0]*width)
    for i in instructions:
        process_instruction(i, grid, width, height)
    on = 0
    for row in grid:
        for col in row:
            if col == 1:
                on += 1
    return on

@runner("Day 8", "Part 2")
def solve_part2(instructions: list[str], width: int, height: int):
    """part 2 solving function"""
    grid = []
    for _ in range(height):
        grid.append([0]*width)
    for i in instructions:
        process_instruction(i, grid, width, height)
    for row in grid:
        out = ""
        for col in row:
            if col == 1:
                out += "#"
            else:
                out += "."
        print(out)

def process_instruction(i: str, grid: list[list[int]], width: int, height: int):
    """apply instruction to the grid values"""
    if i.startswith("rect "):
        w, h = map(int, i[5:].split('x'))
        for y in range(h):
            for x in range(w):
                grid[y][x] = 1
    elif i.startswith("rotate column x="):
        col, times = map(int, i[16:].split(' by '))
        times %= height
        current = []
        for row in range(height):
            current.append(grid[row][col])
        updated = [0]*height
        for i in range(height):
            ni = (i + times) % height
            updated[ni] = current[i]
        for row in range(height):
            grid[row][col] = updated[row]
    elif i.startswith("rotate row y="):
        row, times = map(int, i[13:].split(' by '))
        updated = [0]*width
        for i in range(width):
            ni = (i + times) % width
            updated[ni] = grid[row][i]
        grid[row] = updated

# Data
data = read_lines("input/day08/input.txt")
sample = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1""".splitlines()

# Part 1
assert solve_part1(sample, 7, 3) == 6
assert solve_part1(data, 50, 6) == 128

# Part 2
solve_part2(data, 50, 6)
