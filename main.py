from src.bootstrap.app import AppInitializer
from src.bootstrap.server import ServerRunner


def main() -> None:
    ServerRunner(AppInitializer()).run_server()


if __name__ == "__main__":
    main()
