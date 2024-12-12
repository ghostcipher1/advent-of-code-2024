from typing import List
from src.helpers.io import read_input, parse_lines


class RuleChecker:
    def __init__(self):
        self.above_threshold = False
        self.is_ascending = []
        self.is_descending = []

    def check_constraints(self, values: List[str]):
        for index, current in enumerate(values):
            next_index = index + 1
            if next_index < len(values):
                first_number = int(current)
                second_number = int(values[next_index])
                diff = abs(first_number - second_number)
                self.is_ascending.append(first_number > second_number)
                self.is_descending.append(first_number < second_number)
                if diff == 0 or diff > 3:
                    self.above_threshold = True

    def check_consistency(self) -> bool:
        ascending_only = all(self.is_ascending) and not any(self.is_descending)
        descending_only = all(self.is_descending) and not any(self.is_ascending)
        return ascending_only or descending_only

    def is_safe(self, values: List[str]) -> bool:
        self.check_constraints(values)
        if not self.above_threshold and self.check_consistency():
            return True
        # Additional check: Remove one element to satisfy rules
        for i in range(len(values)):
            self.reset()
            reduced_values = [v for j, v in enumerate(values) if j != i]
            self.check_constraints(reduced_values)
            if not self.above_threshold and self.check_consistency():
                return True
        return False

    def reset(self):
        self.above_threshold = False
        self.is_ascending = []
        self.is_descending = []


def process_value(values: List[List[str]], check_partial: bool = False) -> int:
    result_sum = 0
    for value in values:
        checker = RuleChecker()
        if check_partial:
            if checker.is_safe(value):
                result_sum += 1
        else:
            checker.check_constraints(value)
            if not checker.above_threshold and checker.check_consistency():
                result_sum += 1
    return result_sum


async def part1(input_data: str) -> int:
    data = await read_input(input_data)
    lines = parse_lines(data)
    arr = [line.split(' ') for line in lines]
    return process_value(arr, check_partial=False)


async def part2(input_data: str) -> int:
    data = await read_input(input_data)
    lines = parse_lines(data)
    arr = [line.split(' ') for line in lines]
    return process_value(arr, check_partial=True)
