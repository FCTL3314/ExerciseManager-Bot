from src.config.types import ExerciseValidationSettings
from src.services.duration import parse_duration_string


async def is_name_valid(name: str, settings: ExerciseValidationSettings) -> bool:
    return settings.name_min_length <= len(name) <= settings.name_max_length


async def is_exercise_duration_valid(
    duration_string: str, settings: ExerciseValidationSettings
) -> bool:
    duration = await parse_duration_string(duration_string)
    return settings.max_exercise_duration > duration


async def is_exercise_break_time_valid(
    break_time_string: str, settings: ExerciseValidationSettings
) -> bool:
    break_time = await parse_duration_string(break_time_string)
    return settings.max_exercise_break_time > break_time
