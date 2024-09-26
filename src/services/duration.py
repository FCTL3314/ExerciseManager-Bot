import re
from datetime import timedelta

from src.services.exceptions import InvalidDurationStringError


def to_nanoseconds(duration: timedelta) -> int:
    return int(duration.total_seconds() * 1_000_000_000)


def from_nanoseconds(nanoseconds: int) -> timedelta:
    seconds = nanoseconds / 1_000_000_000
    return timedelta(seconds=seconds)


def parse_duration_string(time_str: str) -> timedelta:
    try:
        pattern = re.compile(r"(?P<value>\d+)(?P<unit>[smhd])")

        matches = pattern.finditer(time_str)
        delta = timedelta()

        units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}

        for match in matches:
            value = int(match.group("value"))
            unit = match.group("unit")
            delta += timedelta(**{units[unit]: value})

        return delta
    except (ValueError, KeyError, AttributeError, TypeError):
        raise InvalidDurationStringError
