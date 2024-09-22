from dataclasses import dataclass


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
class UserValidationConfig:
    username_max_length: int
    username_min_length: int

    password_max_length: int
    password_min_length: int


@dataclass(frozen=True)
class ValidationSettings:
    user: UserValidationConfig


@dataclass(frozen=True)
class Settings:
    logging: LoggingSettings
    validation: ValidationSettings


@dataclass(frozen=True)
class Config:
    env: EnvironmentConfig
    settings: Settings
