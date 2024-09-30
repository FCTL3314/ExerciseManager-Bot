from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.keyboards.inline.exercise import (
    get_skip_exercise_description_keyboard,
    get_skip_exercise_image_keyboard,
)
from src.bot.services.shortcuts.commands import (
    ADD_EXERCISE_COMMAND,
    START_WORKOUT_COMMAND,
)
from src.bot.services.shortcuts.message_templates import (
    ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
    ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
    INVALID_EXERCISE_NAME_MESSAGE,
    INVALID_URL_MESSAGE,
)
from src.bot.services.workout import send_select_workout_keyboard_or_error_message
from src.bot.states.workout import ExerciseAddingStates
from src.config import Settings
from src.services.business.workouts import WorkoutServiceProto
from src.services.validators import is_valid_url
from src.services.validators.duration import is_valid_duration_string
from src.services.validators.exercise import (
    is_name_valid as is_exercise_name_valid,
    is_exercise_duration_valid,
    is_exercise_break_time_valid,
)


@router.message(ADD_EXERCISE_COMMAND.filter())
async def command_add_exercise_handler(
    message: Message,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
    settings: Settings,
) -> None:
    await send_select_workout_keyboard_or_error_message(
        text=ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
        no_workouts_message=ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
        message=message,
        user_id=message.from_user.id,
        workout_service=workout_service,
        limit=settings.pagination.workout.workouts_keyboard_paginate_by,
        buttons_per_row=settings.pagination.workout.workouts_keyboard_buttons_per_row,
    )
    await state.set_state(ExerciseAddingStates.waiting_for_workout_selection)


@router.message(ExerciseAddingStates.waiting_for_name_input)
async def process_add_exercise_name(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    name = message.text.strip()
    if not await is_exercise_name_valid(name, settings.validation.exercise):
        await message.answer(
            INVALID_EXERCISE_NAME_MESSAGE.format(
                min_length=settings.validation.exercise.name_min_length,
                max_length=settings.validation.exercise.name_max_length,
            ),
        )
        return

    await state.update_data(name=name)
    await state.set_state(ExerciseAddingStates.waiting_for_description_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f"🔹 {html.bold("Шаг 2:")} Пожалуйста, опишите ваше упражнение (это необязательно, но поможет вам лучше организоваться):",
        reply_markup=await get_skip_exercise_description_keyboard(),
    )


@router.message(ExerciseAddingStates.waiting_for_description_input)
async def process_add_exercise_description(message: Message, state: FSMContext) -> None:
    description = message.text.strip()

    await state.update_data(description=description)
    await state.set_state(ExerciseAddingStates.waiting_for_image_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f"{html.bold('Шаг 3:')} Теперь введите URL изображения. "
        f"Если у вас нет изображения, просто нажмите {html.bold("Пропустить")}.",
        reply_markup=await get_skip_exercise_image_keyboard(),
    )


@router.message(ExerciseAddingStates.waiting_for_image_input)
async def process_add_exercise_image(message: Message, state: FSMContext) -> None:
    image = message.text.strip()
    if not await is_valid_url(image):
        await message.answer(INVALID_URL_MESSAGE)
        return

    await state.update_data(image=image)
    await state.set_state(ExerciseAddingStates.waiting_for_duration_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f" {html.bold("Шаг 4:")} Теперь введите продолжительность выполнения упражнения. Например, {html.bold('1m')} для 1 минуты или {html.bold('30s')} для 30 секунд:"
    )


@router.message(ExerciseAddingStates.waiting_for_duration_input)
async def process_add_exercise_duration(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    duration = message.text.strip()

    if not await is_valid_duration_string(duration):
        await message.answer(
            f"❌ Неверный формат продолжительности упражнения. Пожалуйста, введите продолжительность снова, используя формат {html.bold('1m')} или {html.bold('30s')}:"
        )
        return

    if not await is_exercise_duration_valid(duration, settings.validation.exercise):
        await message.answer(
            f"❌ Продолжительность упражнения слишком длинная. Пожалуйста, введите меньшую длительность:"
        )
        await state.set_state(ExerciseAddingStates.waiting_for_duration_input)
        return

    await state.update_data(duration=duration)
    await state.set_state(ExerciseAddingStates.waiting_for_break_time_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f"🔹 {html.bold("Шаг 5:")} Теперь введите перерыв после этого упражнения. Например, {html.bold('1m')} для 1 минуты или {html.bold('30s')} для 30 секунд:"
    )


@router.message(ExerciseAddingStates.waiting_for_break_time_input)
async def process_add_exercise_break_time(
    message: Message,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
    settings: Settings,
) -> None:
    data = await state.get_data()

    workout_id = data["workout_id"]
    name = data["name"]
    description = data.get("description")  # TODO: Move none to empty string to backend
    image = data.get("image")
    duration = data["duration"]
    break_time = message.text.strip()

    if not await is_valid_duration_string(break_time):
        await message.answer(
            f"❌ Неверный формат перерыва после упражнения. Пожалуйста, введите перерыв заново, используя формат {html.bold('1m')} или {html.bold('30s')}:"
        )
        return

    if not await is_exercise_break_time_valid(break_time, settings.validation.exercise):
        await message.answer(
            f"❌ Время перерыва слишком длинное. Пожалуйста, введите меньшее время, используя формат {html.bold('1m')} или {html.bold('30s')}:"
        )
        await state.set_state(ExerciseAddingStates.waiting_for_break_time_input)
        return

    await workout_service.add_exercise(
        user_id=message.from_user.id,
        workout_id=workout_id,
        name=name,
        description=description,
        image=image,
        duration=duration,
        break_time=break_time,
    )

    await state.clear()
    await message.answer(
        f"✅ Упражнение успешно добавлено! 🎉\nТеперь вы можете начать тренировку({html.bold(START_WORKOUT_COMMAND)}) или добавить ещё несколько упражнений."
    )
