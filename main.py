import asyncio

from src.bootstrap.app import AppStarter


async def main() -> None:
    await AppStarter().start_app()


if __name__ == "__main__":
    asyncio.run(main())
