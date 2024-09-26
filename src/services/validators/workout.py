from src.config.types import WorkoutValidationSettings


def is_name_valid(name: str, settings: WorkoutValidationSettings) -> bool:
    return settings.name_min_length <= len(name) <= settings.name_max_length
