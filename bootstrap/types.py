from dataclasses import dataclass

from config.types import EnvironmentConfig
from database import IKeyValueRepository


@dataclass
class App:
    config: EnvironmentConfig
    storage: IKeyValueRepository