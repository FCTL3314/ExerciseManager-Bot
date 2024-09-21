from dataclasses import dataclass


@dataclass(frozen=True)
class BotConfig:
    token: str


@dataclass(frozen=True)
class RedisConfig:
    host: str
    port: int


@dataclass(frozen=True)
class EnvironmentConfig:
    bot: BotConfig
    redis: RedisConfig


@dataclass(frozen=True)
class Config:
    env: EnvironmentConfig
