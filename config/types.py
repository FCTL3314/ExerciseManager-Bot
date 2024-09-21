from dataclasses import dataclass


@dataclass(frozen=True)
class BotConfig:
    token: str


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
    redis: RedisConfig

@dataclass(frozen=True)
class Settings:
    ...

@dataclass(frozen=True)
class Config:
    env: EnvironmentConfig
    settings: Settings
