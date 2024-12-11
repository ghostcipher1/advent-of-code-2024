from typing import Any, List, Tuple, TypeVar, Union

T = TypeVar("T", int, str)

def is_number(value: Any) -> bool:
    return isinstance(value, (int, float))

def is_string(value: Any) -> bool:
    return isinstance(value, str)

def is_boolean(value: Any) -> bool:
    return isinstance(value, bool)

def is_object(value: Any) -> bool:
    return isinstance(value, dict)

def sum_numbers(numbers: List[Union[int, float]]) -> Union[int, float]:
    """
    Sums a list of numbers.
    """
    return sum(numbers)

def unique(arr: List[Any]) -> List[Any]:
    """
    Returns a list of unique elements.
    """
    return list(set(arr))

def asc(a: T, b: T) -> int:
    """
    Sorts values in ascending order.
    """
    if is_number(a) and is_number(b):
        return a - b
    elif is_string(a) and is_string(b):
        return (a > b) - (a < b)  # Python equivalent to localeCompare
    raise ValueError("Invalid argument types")

def desc(a: T, b: T) -> int:
    """
    Sorts values in descending order.
    """
    if is_number(a) and is_number(b):
        return b - a
    elif is_string(a) and is_string(b):
        return (b > a) - (b < a)  # Python equivalent to reverse localeCompare
    raise ValueError("Invalid argument types")

def is_between(x: Union[int, float], range_: Tuple[Union[int, float], Union[int, float]]) -> bool:
    """
    Checks if a number is between a given range (inclusive).
    """
    min_, max_ = range_
    return min_ <= x <= max_
