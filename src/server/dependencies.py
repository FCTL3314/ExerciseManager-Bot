from logging import Logger

from aiogram import Dispatcher
from fastapi import Request, Depends

from src.bot.types import Bot
from src.config import Config


async def get_config(request: Request) -> Config:
    return request.state.config


config_dependency = Depends(get_config)


async def get_dispatcher(request: Request) -> Dispatcher:
    return request.state.dp


dispatcher_dependency = Depends(get_dispatcher)


async def get_bot(request: Request) -> Bot:
    return request.state.bot


bot_dependency = Depends(get_bot)


async def get_logger(request: Request) -> Logger:
    return request.state.logger


logger_dependency = Depends(get_logger)
