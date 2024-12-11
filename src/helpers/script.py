from typing import Callable, Tuple, Any
from src.helpers.index import is_between


def format_day(day: int | str) -> str:
    """
    Formats a day as a two-digit string.
    """
    parsed_day = int(day)
    return str(parsed_day).zfill(2)


def format_day_name(day: int | str) -> str:
    """
    Formats a day as `day-XX`.
    """
    try:
        formatted_day = (format_day(day))
    except ValueError:
        raise ValueError(f"Invalid day format: {day}")
    except TypeError:
        raise TypeError(f"Unsupported type for day: {type(day)}")

    return f"day-{formatted_day:02}"  # Ensure zero-padded two-digit format



def validate_day(day: int | str) -> bool:
    """
    Validates if the day is between 1 and 25.
    """
    try:
        parsed_day = int(day)
        return day and not (parsed_day is None) and is_between(parsed_day, (1, 25))
    except ValueError:
        return False


def generate_template(day: int) -> str:
    """
    Generates a template string for a day's code file.
    """
    return f"""from io import parse_lines, read_input

input_data = await read_input('{format_day_name(day)}')

# part1_utils = {{
#     "example_function": lambda x: x  # Example utility function
# }}

def part1():
    lines = parse_lines(input_data)
    # Your code goes here
    return len(lines)
"""


def with_performance(handler: Callable[[], Any]) -> Tuple[Any, float]:
    """
    Measures the performance of a handler function.

    :param handler: A function to execute and measure.
    :return: A tuple of the result and the execution time in milliseconds.
    """
    import time
    start = time.perf_counter()
    result = handler()
    end = time.perf_counter()
    return result, (end - start) * 1000  # Convert seconds to milliseconds


def format_performance(time: float) -> str:
    """
    Formats performance time in milliseconds or microseconds.
    """
    def round_value(x: float) -> float:
        return round((x + 1e-9) * 100) / 100

    if time < 1:
        return f"{round_value(time * 1000)} µs"
    return f"{round_value(time)} ms"


async def is_ok(response) -> None:
    """
    Checks if an HTTP response is OK (status code 200-299).
    """
    if not response.ok:
        raise Exception(f"HTTP request failed with status code {response.status_code}")
