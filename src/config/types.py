from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class BotConfig:
    token: str


@dataclass(frozen=True)
class APIConfig:
    base_url: str


@dataclass(frozen=True)
class RedisConfig:
    host: str
    port: int

    @property
    def uri(self) -> str:
        return f"redis://{self.host}:{self.port}/1"


@dataclass(frozen=True)
class EnvironmentConfig:
    bot: BotConfig
    api: APIConfig
    redis: RedisConfig


@dataclass(frozen=True)
class LoggingSettings:
    format: str


@dataclass(frozen=True)
class UserValidationSettings:
    username_max_length: int
    username_min_length: int

    password_max_length: int
    password_min_length: int


@dataclass(frozen=True)
class WorkoutValidationSettings:
    name_max_length: int
    name_min_length: int


@dataclass(frozen=True)
class ExerciseValidationSettings:
    name_max_length: int
    name_min_length: int
    max_exercise_duration: timedelta
    max_exercise_break_time: timedelta


@dataclass(frozen=True)
class ValidationSettings:
    user: UserValidationSettings
    workout: WorkoutValidationSettings
    exercise: ExerciseValidationSettings


@dataclass(frozen=True)
class LocalizationSettings:
    locales_path: str
    default_locale: str
    domain: str


@dataclass(frozen=True)
class WorkoutPaginationSettings:
    workouts_keyboard_paginate_by: int
    workouts_keyboard_buttons_per_row: int


@dataclass(frozen=True)
class PaginationSettings:
    workout: WorkoutPaginationSettings


@dataclass(frozen=True)
class Settings:
    logging: LoggingSettings
    validation: ValidationSettings
    pagination: PaginationSettings
    localization: LocalizationSettings


@dataclass(frozen=True)
class Config:
    env: EnvironmentConfig
    settings: Settings
