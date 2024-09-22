from src.config.types import UserValidationConfig


def is_username_valid(username: str, settings: UserValidationConfig) -> bool:
    return settings.username_min_length <= len(username) <= settings.username_max_length


def is_password_valid(password: str, settings: UserValidationConfig) -> bool:
    return settings.password_min_length <= len(password) <= settings.password_max_length
