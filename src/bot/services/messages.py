import mimetypes

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

