import asyncio

from bootstrap.app import Bootstrap


async def main() -> None:
    app = Bootstrap().initialize_app()
    await app.storage.set("test", 1)
    test = await app.storage.get("test")


if __name__ == "__main__":
    asyncio.run(main())
