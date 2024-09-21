from config import ISettingsLoader, Settings


class SettingsLoader(ISettingsLoader):

    def load(self) -> Settings:
        ...
