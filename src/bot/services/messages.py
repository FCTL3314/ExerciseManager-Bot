import mimetypes
from collections.abc import Callable

from aiogram.types import Message


async def get_send_method_by_mimetype(mimetype: str | None) -> Callable:
    if mimetype is None:
        return Message.answer_document

    if mimetype.startswith("image/gif"):
        return Message.answer_animation
    elif mimetype == "image/":
        return Message.answer_photo
    elif mimetype.startswith("video/"):
        return Message.answer_video
    elif mimetype.startswith("audio/"):
        return Message.answer_audio
    else:
        return Message.answer_document


async def get_send_method_by_url(url: str) -> Callable:
    mimetype = mimetypes.guess_type(url)[0]
    return await get_send_method_by_mimetype(mimetype)


async def get_file_arg_name_by_method(method: Callable) -> str:
    return {
        Message.answer_photo.__name__: "photo",
        Message.answer_animation.__name__: "animation",
        Message.answer_video.__name__: "video",
        Message.answer_audio.__name__: "audio",
        Message.answer_document.__name__: "document",
    }[method.__name__]


async def send_file_by_url(message: Message, url: str, *args, **kwargs):
    method = await get_send_method_by_url(url)
    file_arg_name = await get_file_arg_name_by_method(method)
    kwargs.update({file_arg_name: url})
    return await method(message, *args, **kwargs)
