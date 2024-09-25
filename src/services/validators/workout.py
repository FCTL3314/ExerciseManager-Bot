from src.config.types import WorkoutValidationConfig


def is_name_valid(username: str, settings: WorkoutValidationConfig) -> bool:
    return settings.name_min_length <= len(username) <= settings.name_max_length
