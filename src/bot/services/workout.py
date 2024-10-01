from aiogram.types import Message

from src.bot.enums import MessageAction
from src.bot.keyboards.inline.workouts import (
    create_select_workout_keyboard,
)
from src.services.business.workouts import WorkoutServiceProto
from src.services.exceptions import NoWorkoutsError


async def send_select_workout_keyboard(
    text: str,
    message: Message,
    user_id: int,
    workout_service: WorkoutServiceProto,
    buttons_per_row: int,
    limit: int,
    offset: int = 0,
    message_action: MessageAction = MessageAction.send,
    show_loading_message: bool = True,
) -> None:
    loading_message = None
    loading_text = "⏳ Загрузка тренировок..."
    if message_action == MessageAction.send and show_loading_message:
        loading_message = await message.answer(loading_text)
    if message_action == MessageAction.edit and show_loading_message:
        loading_message = await message.edit_text(loading_text)

    keyboard = await create_select_workout_keyboard(
        user_id=user_id,
        workout_service=workout_service,
        buttons_per_row=buttons_per_row,
        limit=limit,
        offset=offset,
    )

    if loading_message is not None:
        await loading_message.edit_text(text, reply_markup=keyboard)
        return

    if message_action == MessageAction.send:
        await message.answer(text, reply_markup=keyboard)
    elif message_action == MessageAction.edit:
        await message.edit_text(text, reply_markup=keyboard)


async def send_select_workout_keyboard_or_error_message(
    text: str,
    no_workouts_message: str,
    message: Message,
    user_id: int,
    workout_service: WorkoutServiceProto,
    buttons_per_row: int,
    limit: int,
    offset: int = 0,
    message_action: MessageAction = MessageAction.send,
    show_loading_message: bool = True,
) -> None:

    try:
        await send_select_workout_keyboard(
            text,
            message,
            user_id,
            workout_service,
            buttons_per_row,
            limit,
            offset,
            message_action,
            show_loading_message,
        )
    except NoWorkoutsError:
        if message_action == MessageAction.send:
            await message.answer(no_workouts_message)
        elif message_action == MessageAction.edit:
            await message.edit_text(no_workouts_message)
