import asyncio
import mimetypes
import time
from typing import Callable, Awaitable, Any, Iterable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message


def get_file_type_by_mimetype(mimetype: str) -> str:
    if not isinstance(mimetype, str):
        raise TypeError("mimetype must be a string")

    if mimetype == "image/gif":
        return "animation"
    elif mimetype.startswith("image/"):
        return "photo"
    elif mimetype.startswith("video/"):
        return "video"
    elif mimetype.startswith("audio/"):
        return "audio"
    else:
        return "document"


def get_message_type_by_url(url: str) -> str | None:
    mimetype, _ = mimetypes.guess_type(url)

    if mimetype is None:
        return None

    return get_file_type_by_mimetype(mimetype)


async def send_message_by_file_type(message: Message, url: str, **kwargs) -> Message:
    message_type = get_message_type_by_url(url)

    if message_type is None:
        message_type = "text"

    match message_type:
        case "photo":
            return await message.answer_photo(photo=url, **kwargs)
        case "animation":
            return await message.answer_animation(animation=url, **kwargs)
        case "video":
            return await message.answer_video(video=url, **kwargs)
        case "audio":
            return await message.answer_audio(audio=url, **kwargs)
        case "document":
            return await message.answer_document(document=url, **kwargs)
        case _:
            return await message.answer(text=url, **kwargs)


async def run_timer(
    seconds: int,
    on_tick: Callable[..., Awaitable[Any]],
    state: FSMContext,
    stop_states: Iterable[StatesGroup] = None,
    pause_states: Iterable[StatesGroup] = None,
) -> Any:
    previous_tick_result = None
    remaining_seconds = seconds

    while remaining_seconds >= 0:
        start_time = time.monotonic()
        current_state = await state.get_state()

        if stop_states and current_state in stop_states:
            return previous_tick_result

        if pause_states and current_state in pause_states:
            while await state.get_state() in pause_states:
                await asyncio.sleep(1)

        previous_tick_result = await on_tick(
            **{
                "iteration": seconds - remaining_seconds,
                "second": remaining_seconds,
                "previous_tick_result": previous_tick_result,
            }
        )
        end_time = time.monotonic()

        elapsed_time = end_time - start_time
        remaining_seconds -= int(elapsed_time)

        remaining_sleep_time = 1 - (elapsed_time % 1)

        if remaining_sleep_time > 0 and remaining_seconds > 0:
            await asyncio.sleep(remaining_sleep_time)

        remaining_seconds -= 1

    return previous_tick_result
