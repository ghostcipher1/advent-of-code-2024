from io import parse_lines, read_input

input_data = await read_input('day-03')

# part1_utils = {
#     "example_function": lambda x: x  # Example utility function
# }

def part1():
    lines = parse_lines(input_data)
    # Your code goes here
    return len(lines)
