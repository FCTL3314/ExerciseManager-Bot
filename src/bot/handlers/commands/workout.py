from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.services.shortcuts.commands import (
    ADD_WORKOUT_COMMAND,
    START_WORKOUT_COMMAND,
)
from src.bot.services.shortcuts.message_templates import (
    INVALID_WORKOUT_NAME_MESSAGE,
    START_WORKOUT_WORKOUT_SELECTION_MESSAGE,
    START_WORKOUT_NO_WORKOUTS_MESSAGE,
)
from src.bot.services.workout import send_select_workout_keyboard_or_error_message
from src.bot.states.workout import (
    WorkoutAddingStates,
    StartWorkoutStates,
)
from src.config import Settings
from src.services.business.workouts import WorkoutServiceProto
from src.services.validators.workout import is_name_valid as is_workout_name_valid


@router.message(ADD_WORKOUT_COMMAND.filter())
async def command_add_workout_handler(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    await state.set_state(WorkoutAddingStates.waiting_for_name_input)
    await message.answer(
        "Давайте начнем создание новой тренировки! 🏋️‍♂️\n\n"
        f"1️⃣ Пожалуйста, введите название тренировки (от {settings.validation.workout.name_min_length} до "
        f"{settings.validation.workout.name_max_length} символов):"
    )


@router.message(WorkoutAddingStates.waiting_for_name_input)
async def process_add_workout_name(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    name = message.text.strip()
    if not await is_workout_name_valid(name, settings.validation.workout):
        await message.answer(
            INVALID_WORKOUT_NAME_MESSAGE.format(
                min_length=settings.validation.workout.name_min_length,
                max_length=settings.validation.workout.name_max_length,
            ),
        )
        return

    await state.update_data(name=name)
    await state.set_state(WorkoutAddingStates.waiting_for_description_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        "2️⃣ Пожалуйста, опишите вашу тренировку (это необязательно, но поможет вам лучше организоваться):"
    )


@router.message(WorkoutAddingStates.waiting_for_description_input)
async def process_add_workout_description(
    message: Message, state: FSMContext, workout_service: WorkoutServiceProto
) -> None:
    data = await state.get_data()

    name = data["name"]
    description = message.text.strip()

    await workout_service.create(
        user_id=message.from_user.id, name=name, description=description
    )

    await state.clear()
    await message.answer(
        "🎉 Тренировка успешно создана! Теперь вы можете добавлять упражнения к этой тренировке."
    )


@router.message(START_WORKOUT_COMMAND.filter())
async def command_start_workout_handler(
    message: Message,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
    settings: Settings,
) -> None:
    await send_select_workout_keyboard_or_error_message(
        text=START_WORKOUT_WORKOUT_SELECTION_MESSAGE,
        no_workouts_message=START_WORKOUT_NO_WORKOUTS_MESSAGE,
        message=message,
        user_id=message.from_user.id,
        workout_service=workout_service,
        limit=settings.pagination.workout.workouts_keyboard_paginate_by,
        buttons_per_row=settings.pagination.workout.workouts_keyboard_buttons_per_row,
    )
    await state.set_state(StartWorkoutStates.waiting_for_workout_selection)
