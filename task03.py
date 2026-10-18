"""Command-line log analyzer for the homework task 3."""

import argparse
from datetime import datetime


LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    """Parse one line into date, time, level, and message."""
    parts = line.strip().split(maxsplit=3)
    if len(parts) != 4:
        raise ValueError("expected DATE TIME LEVEL MESSAGE")

    date, time, level, message = parts

    try:
        datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    except ValueError as exc:
        raise ValueError("invalid date or time") from exc

    if level not in LOG_LEVELS:
        raise ValueError(f"unknown logging level: {level}")

    return {
        "date": date,
        "time": time,
        "level": level,
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """Read log records from a UTF-8 file, reporting malformed line numbers."""
    logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as exc:
                raise ValueError(f"line {line_number}: {exc}") from exc
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Return records with the specified level (case-insensitive)."""
    return [log for log in logs if log["level"] == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    """Count records for each supported logging level."""
    counts = {level: 0 for level in LOG_LEVELS}
    for log in logs:
        counts[log["level"]] += 1
    return counts


def display_log_counts(counts: dict) -> None:
    """Print a formatted summary table."""
    print(f"{'Рівень логування':<18} | Кількість")
    print(f"{'-' * 18}-|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<18} | {count}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a log file.")
    parser.add_argument("file_path", help="Path to a log file")
    parser.add_argument("level", nargs="?", help="Optional logging level")
    args = parser.parse_args()

    if args.level and args.level.upper() not in LOG_LEVELS:
        parser.error(f"level must be one of: {', '.join(LOG_LEVELS)}")

    try:
        logs = load_logs(args.file_path)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"Помилка читання логів: {exc}")
        return 1

    display_log_counts(count_logs_by_level(logs))

    if args.level:
        level = args.level.upper()
        print(f"\nДеталі логів для рівня '{level}':")
        matching_logs = filter_logs_by_level(logs, level)
        if not matching_logs:
            print("Записів немає.")
        for log in matching_logs:
            print(f"{log['date']} {log['time']} - {log['message']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
