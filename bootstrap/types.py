from dataclasses import dataclass

from config.types import EnvironmentConfig


@dataclass
class App:
    config: EnvironmentConfig