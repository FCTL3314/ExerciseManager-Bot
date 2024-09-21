import asyncio

from bootstrap.app import Bootstrap


async def main() -> None:
    app = Bootstrap().initialize_app()
    return await app.bot.dp.start_polling(app.bot.client)


if __name__ == "__main__":
    asyncio.run(main())
