import sys
import json
import datetime
import asyncio
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import importlib
import logging

from src.helpers.script import format_day_name, format_day, validate_day

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("run_day")


def get_results_file_path():
    return Path("./results.json")


async def run_day(day, input_file=None, is_dev_mode=False, is_watch_mode=False):
    if not validate_day(day):
        logger.error("🎅 Pick a day between 1 and 25.")
        logger.info("🎅 To get started, try: python main.py 1")
        return

    # Ensure input_file retains its value if provided
    input_file = input_file if input_file else f"{format_day_name(day)}"

    file_path = Path(f"./src/{format_day_name(day)}/index.py")

    if not file_path.exists():
        logger.error(f"Day {format_day(day)} does not exist!")
        return

    captured_logs = []

    def intercept_log(message):
        captured_logs.append(message)
        logger.info(message)

    try:
        module = importlib.import_module(f"src.{format_day_name(day)}.index")
        part1 = getattr(module, "part1", None)
        part2 = getattr(module, "part2", None)

        one = None
        one_performance = 0
        two = None
        two_performance = 0

        if callable(part1):
            start_time = datetime.datetime.utcnow()
            if asyncio.iscoroutinefunction(part1):
                one = await part1(input_file)
            else:
                one = part1(input_file)
            one_performance = (datetime.datetime.utcnow() - start_time).total_seconds() * 1000

        if callable(part2):
            start_time = datetime.datetime.utcnow()
            if asyncio.iscoroutinefunction(part2):
                two = await part2(input_file)
            else:
                two = part2(input_file)
            two_performance = (datetime.datetime.utcnow() - start_time).total_seconds() * 1000

        day_results = {
            f"day{day}": {
                "part1": {
                    "solved": bool(one),
                    "date": one and datetime.datetime.utcnow().isoformat(),
                    "performance": f"{one_performance:.2f} ms",
                },
                "part2": {
                    "solved": bool(two),
                    "date": two and datetime.datetime.utcnow().isoformat(),
                    "performance": f"{two_performance:.2f} ms",
                },
            }
        }

        if not is_watch_mode:
            results_file_path = get_results_file_path()
            all_results = {}

            if results_file_path.exists():
                try:
                    with results_file_path.open("r", encoding="utf-8") as f:
                        all_results = json.load(f)
                except json.JSONDecodeError:
                    logger.warning("Creating a new results.json file...")

            all_results.update(day_results)

            with results_file_path.open("w", encoding="utf-8") as f:
                json.dump(all_results, f, indent=2)

            logger.info(f"✅ Results saved to {results_file_path}")

        if is_watch_mode:
            logger.info("🖨️ Console Logs During Execution:")
            for log in captured_logs:
                logger.info(log)
        else:
            logger.info(f"🌲 Part One: {one or '—'} ({one_performance:.2f} µs)")
            logger.info(f"🎄 Part Two: {two or '—'} ({two_performance:.2f} µs)")

    except Exception as error:
        logger.error(f"❌ Error during execution: {error}")


if __name__ == "__main__":
    try:
        day = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.datetime.now().day
        day_name = format_day_name(day)
        input_file = sys.argv[2] if len(sys.argv) > 2 else f"./src/{day_name}/input.txt"
    except ValueError:
        logger.error("The provided day must be an integer.")
        sys.exit(1)

    is_dev_mode = "--dev" in sys.argv
    is_watch_mode = "--watch" in sys.argv

    if is_watch_mode:
        logger.info("🔁 Watch mode enabled...")


        class ReloadHandler(FileSystemEventHandler):
            def __init__(self, day):
                self.day = day

            def on_modified(self, event):
                if event.src_path.endswith(f"/{format_day_name(self.day)}/index.py"):
                    logger.info(f"♻️ Reloading Day {self.day}...")
                    asyncio.run(run_day(self.day, is_dev_mode=True, is_watch_mode=True))


        observer = Observer()
        observer.schedule(ReloadHandler(day), path=f"./src/{format_day_name(day)}", recursive=False)
        observer.start()

        try:
            logger.info("👀 Watching for file changes...")
            while True:
                pass
        except KeyboardInterrupt:
            observer.stop()
            logger.info("🛑 Stopping watch mode.")
        observer.join()
    else:

        asyncio.run(run_day(day, input_file, is_dev_mode, is_watch_mode))
