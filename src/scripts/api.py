import os
import requests


def get_session_cookie() -> str:
    """
    Retrieves the session cookie from the environment variable.
    """
    session = os.getenv("SESSION")
    if not session:
        raise ValueError("SESSION environment variable is not set. Please set it to authenticate.")
    return session


def fetch_input(day: int, year: int = None) -> str:
    """
    Fetches the input for a given day and year from the Advent of Code website.

    :param day: The day number for which to fetch input.
    :param year: The year of the event (defaults to the current year).
    :return: The text content of the input.
    """
    session = get_session_cookie()
    if year is None:
        from datetime import datetime
        year = datetime.now().year

    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {"Cookie": f"session={session}"}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch input. HTTP Status Code: {response.status_code}. "
                        f"Check if your session cookie is valid.")

    return response.text.strip()
