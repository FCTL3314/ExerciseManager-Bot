import re
from datetime import timedelta

from src.services.exceptions import InvalidDurationStringError
from src.services.validators.duration import (
    DURATION_STRING_PATTERN,
    is_valid_duration_string,
)


def to_nanoseconds(duration: timedelta) -> int:
    return int(duration.total_seconds() * 1_000_000_000)


async def ato_nanoseconds(duration: timedelta) -> int:
    return to_nanoseconds(duration)


def from_nanoseconds(nanoseconds: int) -> timedelta:
    seconds = nanoseconds / 1_000_000_000
    return timedelta(seconds=seconds)


async def afrom_nanoseconds(nanoseconds: int) -> timedelta:
    return from_nanoseconds(nanoseconds)


async def parse_duration_string(duration_string: str) -> timedelta:
    try:
        if not await is_valid_duration_string(duration_string):
            raise InvalidDurationStringError

        pattern = re.compile(DURATION_STRING_PATTERN)

        matches = pattern.finditer(duration_string)
        delta = timedelta()

        units = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days"}

        for match in matches:
            value = int(match.group("value"))
            unit = match.group("unit")
            delta += timedelta(**{units[unit]: value})

        return delta
    except (ValueError, KeyError, AttributeError, TypeError):
        raise InvalidDurationStringError
