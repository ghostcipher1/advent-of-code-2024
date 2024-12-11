import sys
import asyncio
from src.scripts.setup_day import setup_day
from src.scripts.run_day import run_day
from src.scripts.api import get_session_cookie, fetch_input

def print_usage():
    print("Usage:")
    print("  python main.py setup <day>        # Set up a new day")
    print("  python main.py fetch <day>        # Fetch input for a day")
    print("  python main.py run <day>          # Run solutions for a day")

def validate_session():
    """
    Validates the SESSION environment variable to ensure authentication is possible.
    """
    try:
        session = get_session_cookie()
        print("✅ Authentication successful. SESSION is set.")
        return True
    except ValueError as e:
        print(f"❌ {e}")
        return False

async def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    command = sys.argv[1].lower()
    day = sys.argv[2]


    if command == "setup":
        # Validate authentication before setting up the day
        if not validate_session():
            print("❌ Authentication failed. Please set the SESSION environment variable.")
            sys.exit(1)

        print(f"Setting up Day {day}...")
        await setup_day(int(day))

    elif command == "fetch":
        # Validate authentication before fetching input
        if not validate_session():
            print("❌ Authentication failed. Please set the SESSION environment variable.")
            sys.exit(1)

        print(f"Fetching input for Day {day}...")
        input_data = await fetch_input(day=int(day))

        print(f"Input fetched:\n{input_data}")

    elif command == "run":
        # Validate authentication before fetching input
        if not validate_session():
            print("❌ Authentication failed. Please set the SESSION environment variable.")
            sys.exit(1)

        print(f"Running solutions for Day {day}...")
        await run_day(int(day))

    else:
        print("Invalid command.")
        print_usage()

if __name__ == "__main__":
    asyncio.run(main())
