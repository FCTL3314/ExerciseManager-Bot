import re


DURATION_STRING_PATTERN = r"(?P<value>\d+)(?P<unit>[smhd])"


def is_valid_duration_string(duration_string: str) -> bool:
    pattern = re.compile(DURATION_STRING_PATTERN)
    return pattern.match(duration_string) is not None