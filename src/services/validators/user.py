from src.config.types import UserValidationSettings


async def is_username_valid(username: str, settings: UserValidationSettings) -> bool:
    return settings.username_min_length <= len(username) <= settings.username_max_length


async def is_password_valid(password: str, settings: UserValidationSettings) -> bool:
    return settings.password_min_length <= len(password) <= settings.password_max_length
