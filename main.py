import asyncio

from bootstrap.app import Bootstrap


async def main() -> None:
    app = Bootstrap().initialize_app()
    return None


if __name__ == "__main__":
    asyncio.run(main())
