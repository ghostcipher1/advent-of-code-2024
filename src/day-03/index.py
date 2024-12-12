# Redefine all necessary components for execution
import re
from typing import List, Pattern
from src.helpers.io import read_input, parse_lines

def clean_input(input_data: str) -> str:
    """
    Filters the input data to include only lines that contain valid `mul(x, y)` patterns.
    """
    valid_lines = []
    regex = re.compile(r"mul\((\d+),(\d+)\)")

    for line in input_data.splitlines():
        if regex.search(line):
            valid_lines.append(line)

    return "\n".join(valid_lines)

def extract_matches(input_data: str, pattern: str) -> List[re.Match]:
    """
    Extract all matches of a given regex pattern from the input data.
    """
    regex = re.compile(pattern)
    return list(regex.finditer(input_data))

async def part1(input_data: str) -> int:
    data = await read_input(input_data)
    lines = parse_lines(data)
    regex_pattern = r"mul\((\d+),(\d+)\)"
    matches = extract_matches(data, regex_pattern)

    sum_result = 0
    for match in matches:
        sum_result += int(match.group(1)) * int(match.group(2))

    return sum_result

class Part2Utils:
    @staticmethod
    def get_arr(input_data: str, regex: Pattern) -> List[int]:
        return [match.start() for match in regex.finditer(input_data)]

    @staticmethod
    def get_last_index(arr: List[int], current_match: re.Match) -> int:
        return max((i for i in arr if i < current_match.start()), default=None)

async def part2(input_data: str) -> int:
    data = await read_input(input_data)
    lines = parse_lines(data)
    regex_pattern = r"mul\((\d+),(\d+)\)"
    do_regex_pattern = r"do\(\)"
    dont_regex_pattern = r"don't\(\)"

    sum_result = 0

    dont_regex = re.compile(dont_regex_pattern)
    do_regex = re.compile(do_regex_pattern)

    dont_arr_index = Part2Utils.get_arr(data, dont_regex)
    do_arr_index = Part2Utils.get_arr(data, do_regex)

    regex = re.compile(regex_pattern)
    for match in regex.finditer(data):
        last_do_index = Part2Utils.get_last_index(do_arr_index, match)
        last_dont_index = Part2Utils.get_last_index(dont_arr_index, match)

        if last_dont_index is None or (last_do_index is not None and last_do_index > last_dont_index):
            sum_result += int(match.group(1)) * int(match.group(2))

    return sum_result
