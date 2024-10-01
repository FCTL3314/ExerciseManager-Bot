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


def get_file_type_by_url(url: str) -> str:
    mimetype, _ = mimetypes.guess_type(url)

    if mimetype is None:
        return "text"

    return get_file_type_by_mimetype(mimetype)


async def send_file_by_url(message: Message, url: str, **kwargs) -> Message:
    file_type = get_file_type_by_url(url)

    if file_type == "photo":
        return await message.answer_photo(photo=url, **kwargs)
    elif file_type == "animation":
        return await message.answer_animation(animation=url, **kwargs)
    elif file_type == "video":
        return await message.answer_video(video=url, **kwargs)
    elif file_type == "audio":
        return await message.answer_audio(audio=url, **kwargs)
    elif file_type == "document":
        return await message.answer_document(document=url, **kwargs)
    else:
        return await message.answer(text=url, **kwargs)
