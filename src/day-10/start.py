import math
from collections import deque

def read_input(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()

def parse_lines(input_str):
    return input_str.splitlines()

def get_starting_points(grid):
    starting_points = []
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 0:
                starting_points.append((row, col))
    return starting_points

def get_grid(lines):
    return [[int(char) for char in line] for line in lines]

directions = [
    (-1, 0),
    (1, 0),
    (0, 1),
    (0, -1),
]

def calculate_trail_head_score(grid, point):
    num_rows = len(grid)
    num_cols = len(grid[0])

    def is_in_bound(row, col):
        return 0 <= row < num_rows and 0 <= col < num_cols

    queue = deque([point])
    reachable_nines = set()
    visited = set()

    while queue:
        row, col, height = queue.popleft()

        if (row, col, height) in visited:
            continue

        visited.add((row, col, height))

        if grid[row][col] == 9:
            reachable_nines.add((row, col, height))
            continue

        for dX, dY in directions:
            new_row, new_col = row + dX, col + dY
            if (
                is_in_bound(new_row, new_col)
                and (new_row, new_col, height + 1) not in visited
                and grid[new_row][new_col] == height + 1
            ):
                queue.append((new_row, new_col, grid[new_row][new_col]))

    return len(reachable_nines)

def part1(input_file):
    input_data = read_input(input_file)
    lines = parse_lines(input_data)

    grid = get_grid(lines)
    starting_points = get_starting_points(grid)

    score = 0
    for point in starting_points:
        score += calculate_trail_head_score(grid, (point[0], point[1], 0))

    print(score)
    return score

class Trail:
    def __init__(self, row, col, path):
        self.row = row
        self.col = col
        self.path = path

def calculate_unique_trails(grid, point):
    num_rows = len(grid)
    num_cols = len(grid[0])

    def is_in_bound(row, col):
        return 0 <= row < num_rows and 0 <= col < num_cols

    queue = deque()
    distinct_trails = set()

    queue.append(Trail(point[0], point[1], f"{point[0]},{point[1]}"))

    while queue:
        trail = queue.pop()
        row, col, path = trail.row, trail.col, trail.path

        if grid[row][col] == 9:
            distinct_trails.add(path)
            continue

        for dX, dY in directions:
            new_row, new_col = row + dX, col + dY
            if (
                is_in_bound(new_row, new_col)
                and grid[row][col] + 1 == grid[new_row][new_col]
            ):
                queue.append(Trail(new_row, new_col, f"{path}->{new_row},{new_col}"))

    return len(distinct_trails)

def part2(input_file):
    input_data = read_input(input_file)
    lines = parse_lines(input_data)

    grid = get_grid(lines)
    starting_points = get_starting_points(grid)

    score = 0
    for point in starting_points:
        score += calculate_unique_trails(grid, point)

    print(score)
    return score
