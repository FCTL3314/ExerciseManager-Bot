from datetime import timedelta


def to_nanoseconds(duration: timedelta) -> int:
    return int(duration.total_seconds() * 1_000_000_000)