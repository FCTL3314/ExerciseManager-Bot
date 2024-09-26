from src.config.types import ExerciseValidationSettings
from src.services.duration import parse_duration_string


def is_name_valid(name: str, settings: ExerciseValidationSettings) -> bool:
    return settings.name_min_length <= len(name) <= settings.name_max_length


def is_exercise_duration_valid(
    duration_string: str, settings: ExerciseValidationSettings
) -> bool:
    duration = parse_duration_string(duration_string)
    return settings.max_exercise_duration > duration


def is_exercise_break_time_valid(
    break_time_string: str, settings: ExerciseValidationSettings
) -> bool:
    break_time = parse_duration_string(break_time_string)
    return settings.max_exercise_break_time > break_time
