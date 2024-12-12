from src.helpers.io import parse_lines, read_input
from collections import Counter



# Solution for Historian Hysteria Puzzle

async def part1(input_file):
    # Read and parse input file
    input_data = await read_input(input_file)
    lines = parse_lines(input_data)

    # Extract and sort arrays
    left_list = sorted([int(line.split()[0]) for line in lines])
    right_list = sorted([int(line.split()[1]) for line in lines])

    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate total distance
    total_distance = sum(abs(l - r) for l, r in zip(left_sorted, right_sorted))
    return total_distance


async def part2(input_file):
    # Read and parse input file
    input_data = await read_input(input_file)
    lines = parse_lines(input_data)

    # Extract and sort arrays
    left_list = sorted([int(line.split()[0]) for line in lines])
    right_list = sorted([int(line.split()[1]) for line in lines])

    # Count occurrences in right list
    right_count = Counter(right_list)

    # Calculate similarity score
    similarity_score = sum(num * right_count[num] for num in left_list)
    return similarity_score
