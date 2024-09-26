from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.keyboards.inline.workouts import get_workouts_keyboard
from src.bot.message_templates import (
    INVALID_WORKOUT_NAME_TEMPLATE,
    INVALID_EXERCISE_NAME_TEMPLATE,
)
from src.bot.services.shortcuts.commands import (
    ADD_WORKOUT_COMMAND,
    ADD_EXERCISE_COMMAND,
)
from src.bot.states import WorkoutAddingStates, ExerciseAddingStates
from src.config import Settings
from src.services.business.workouts import IWorkoutService
from src.services.exceptions import (
    InvalidDurationStringError,
    ExerciseBreakTooLongError,
)
from src.services.validators.exercise import is_name_valid as is_exercise_name_valid
from src.services.validators.workout import is_name_valid as is_workout_name_valid


@router.message(ADD_WORKOUT_COMMAND.as_filter())
async def command_add_workout_handler(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    await state.set_state(WorkoutAddingStates.waiting_for_name_input)
    await message.answer(
        "Давайте создадим новую тренировку! 🏋️‍♂️\n\n"
        f"1️⃣ Введите название тренировки (от {settings.validation.workout.name_min_length} до "
        f"{settings.validation.workout.name_max_length} символов):"
    )


@router.message(WorkoutAddingStates.waiting_for_name_input)
async def process_add_workout_name(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    name = message.text.strip()
    if not is_workout_name_valid(name, settings.validation.workout):
        await message.answer(
            INVALID_WORKOUT_NAME_TEMPLATE.format(
                min_length=settings.validation.workout.name_min_length,
                max_length=settings.validation.workout.name_max_length,
            ),
        )
        return

    await state.update_data(name=name)
    await state.set_state(WorkoutAddingStates.waiting_for_description_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        "2️⃣ Теперь опишите свою тренировку (необязательно, но полезно):"
    )


@router.message(WorkoutAddingStates.waiting_for_description_input)
async def process_add_workout_description(
    message: Message, state: FSMContext, workout_service: IWorkoutService
) -> None:
    data = await state.get_data()

    name = data["name"]
    description = message.text.strip()

    await workout_service.create(
        user_id=message.from_user.id, name=name, description=description
    )

    await state.clear()
    await message.answer(
        "Тренировка успешно создана! 🎉\nТеперь вы можете добавлять упражнения."
    )


@router.message(ADD_EXERCISE_COMMAND.as_filter())
async def command_add_exercise_handler(
    message: Message,
    state: FSMContext,
    workout_service: IWorkoutService,
) -> None:
    workouts = await workout_service.list(user_id=message.from_user.id)
    if not workouts:
        await message.answer(
            f"У вас нет созданных тренировок. Создайте тренировку перед добавлением упражнений({html.bold(ADD_WORKOUT_COMMAND)})."
        )
        return

    keyboard = await get_workouts_keyboard(workouts)
    await state.set_state(ExerciseAddingStates.waiting_for_workout_selection)
    await message.answer(
        "Выберите тренировку, в которую хотите добавить упражнение:",
        reply_markup=keyboard,
    )


@router.message(ExerciseAddingStates.waiting_for_name_input)
async def process_add_exercise_name(
    message: Message, state: FSMContext, settings: Settings
) -> None:
    name = message.text.strip()
    if not is_exercise_name_valid(name, settings.validation.exercise):
        await message.answer(
            INVALID_EXERCISE_NAME_TEMPLATE.format(
                min_length=settings.validation.exercise.name_min_length,
                max_length=settings.validation.exercise.name_max_length,
            ),
        )
        return

    await state.update_data(name=name)
    await state.set_state(ExerciseAddingStates.waiting_for_description_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        "2️⃣ Теперь опишите ваше упражнение (необязательно, но полезно):"
    )


@router.message(ExerciseAddingStates.waiting_for_description_input)
async def process_add_exercise_description(message: Message, state: FSMContext) -> None:
    description = message.text.strip()

    await state.update_data(description=description)
    await state.set_state(ExerciseAddingStates.waiting_for_duration_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f"3️⃣ Теперь введите продолжительность выполнения этого упражнения. Например {html.bold("1m")} или {html.bold("30s")}"
    )


@router.message(ExerciseAddingStates.waiting_for_duration_input)
async def process_add_exercise_description(message: Message, state: FSMContext) -> None:
    duration = message.text.strip()

    await state.update_data(duration=duration)
    await state.set_state(ExerciseAddingStates.waiting_for_break_time_input)
    await message.answer(
        f"Отлично! ✅\n\n"
        f"3️⃣ Теперь введите перерыв после этого упражнения. Например {html.bold("1m")} или {html.bold("30s")}"
    )


@router.message(ExerciseAddingStates.waiting_for_break_time_input)
async def process_add_exercise_break_time(
    message: Message,
    state: FSMContext,
    workout_service: IWorkoutService,
) -> None:
    data = await state.get_data()

    workout_id = data["workout_id"]
    name = data["name"]
    description = data["description"]
    duration = data["duration"]
    break_time = message.text.strip()

    try:
        await workout_service.add_exercise(
            user_id=message.from_user.id,
            workout_id=workout_id,
            name=name,
            description=description,
            duration=duration,
            break_time=break_time,
        )
    except InvalidDurationStringError:
        await state.clear()
        await message.answer(
            "❌ Неверный формат перерыва или продолжительности упражнение."
        )
        return
    except ExerciseBreakTooLongError:
        await state.clear()
        await message.answer("❌ Продолжительность упражнение слишком долгая.")
        return

    await state.clear()
    await message.answer(
        "Упражнение успешно добавлено! 🎉\nТеперь вы можете начать тренировку либо добавить ещё пару упражнений."
    )
