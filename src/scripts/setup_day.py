import os
from pathlib import Path
import datetime
from termcolor import colored
from src.helpers.script import format_day, format_day_name, validate_day, generate_template
from .api import fetch_input

async def setup_day(day: int):
    """
    Sets up the directory and files for a given Advent of Code day.
    """
    if not validate_day(day):
        print(f"🎅 Pick a day between {colored('1', attrs=['bold'])} and {colored('25', attrs=['bold'])} .")
        print(f"🎅 To get started, try: {colored('python setup_day.py 1', attrs=['bold'])}")
        return

    dir_path = Path(f"./src/{format_day_name(day)}")

    if dir_path.exists():
        print(f"{colored(f'Day {day} already exists!', 'red', attrs=['bold'])}")
        return

    current_year = datetime.datetime.now().year
    year = int(os.getenv("YEAR", current_year))

    if not (2015 <= year <= current_year):
        print(f"{colored('Year must be between 2024 and {current_year}', 'red', attrs=['bold'])}")
        return

    print("📄 Fetching input...")
    try:
        input_data = fetch_input(day=day, year=year)
    except Exception as e:
        print("{colored(❌ Fetching input failed, empty file will be created., 'red', attrs=['bold'])}")
        input_data = ""

    print(f"📂 Setting up day {format_day(day)}...")

    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        (dir_path / f"day-{day}.txt").write_text(input_data)
        (dir_path / "start.py").write_text(generate_template(day))
        print(f"{colored(f'Day {day} set up successfully!', 'green', attrs=['bold'])}")
    except Exception as e:
        print(f"{colored(f'Failed to set up day {day}!', 'red', attrs=['bold'])}")


if __name__ == "__main__":
    import sys
    day_arg = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now().day
    setup_day(day_arg)
