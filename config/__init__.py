from config.types import Config as ConfigType

class Config:

    def __init__(self) -> None:
        ...

    def load(self) -> ConfigType:
        ...