from src.config.types import ExerciseValidationSettings


def is_name_valid(name: str, settings: ExerciseValidationSettings) -> bool:
    return settings.name_min_length <= len(name) <= settings.name_max_length
