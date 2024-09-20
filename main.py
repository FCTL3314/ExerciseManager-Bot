from config.environment import EnvironmentConfigLoader


def main() -> None:
    config = EnvironmentConfigLoader().load()
    a = 1

if __name__ == "__main__":
    main()
