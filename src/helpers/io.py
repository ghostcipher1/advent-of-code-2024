from typing import Callable, List, TypeVar, Optional, Union
from pathlib import Path

T = TypeVar("T")  # Generic type for transformations


async def read_file(filepath: str) -> str:
    """
    Reads a file asynchronously and trims its content.

    :param filepath: The path to the file.
    :return: The trimmed content of the file.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    return path.read_text().strip()


async def read_input(dir: str, file_name: str = "input") -> str:
    """
    Reads an input file for a specific day.

    :param dir: The directory or day identifier (e.g., 'day-01').
    :param file_name: The name of the file to read (default: 'input').
    :return: The content of the file.
    """
    filepath = f"./src/{dir}/{file_name}.txt"
    return await read_file(filepath)


def parse_lines(
    input_data: str,
    transform: Optional[Callable[[str], T]] = None,
    include_empty: bool = False,
) -> List[Union[str, T]]:
    """
    Parses a string into lines, optionally transforming them.

    :param input_data: The input string.
    :param transform: An optional transformation function to apply to each line.
    :param include_empty: Whether to include empty lines.
    :return: A list of parsed (and optionally transformed) lines.
    """
    lines = input_data.split("\n")
    if not include_empty:
        lines = list(filter(bool, lines))  # Filter out empty lines
    return [transform(line) for line in lines] if transform else lines


def parse_groups(
    input_data: str, transform: Optional[Callable[[str], T]] = None
) -> List[List[Union[str, T]]]:
    """
    Parses a string into groups of lines separated by blank lines.

    :param input_data: The input string.
    :param transform: An optional transformation function to apply to each line.
    :return: A list of groups, each containing a list of parsed (and optionally transformed) lines.
    """
    groups = input_data.split("\n\n")
    return [parse_lines(group, transform) for group in groups]
