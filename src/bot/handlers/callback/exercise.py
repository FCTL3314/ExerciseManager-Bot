import asyncio

from aiogram import html
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import (
    NextExerciseCallback,
    SkipExerciseDescriptionCallback,
    SkipExerciseImageCallback,
    SkipWorkoutExerciseCallback,
)
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.exercise import create_skip_exercise_image_keyboard
from src.bot.services.exercise import handle_workout_exercise
from src.bot.states.workout import StartWorkoutStates, ExerciseAddingStates
from src.services.business.workouts import WorkoutServiceProto


@router.callback_query(
    StartWorkoutStates.workout_in_progress, NextExerciseCallback.filter()
)
async def process_next_exercise(
    callback_query: CallbackQuery,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    asyncio.create_task(
        handle_workout_exercise(callback_query.message, workout_service, state)
    )
    await callback_query.answer()


@router.callback_query(
    ExerciseAddingStates.waiting_for_description_input,
    SkipExerciseDescriptionCallback.filter(),
)
async def skip_exercise_description(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(ExerciseAddingStates.waiting_for_image_input)
    await callback_query.message.answer(
        f"Отлично! ✅\n\n"  # TODO: Move duplicated message to the templates. (commands/exercise.py:75)
        f"{html.bold('Шаг 3:')} Теперь введите URL изображения. "
        f"Если у вас нет изображения, просто нажмите {html.bold("Пропустить")}.",
        reply_markup=await create_skip_exercise_image_keyboard(),
    )
    await callback_query.answer()


@router.callback_query(
    ExerciseAddingStates.waiting_for_image_input,
    SkipExerciseImageCallback.filter(),
)
async def skip_exercise_image(callback_query: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ExerciseAddingStates.waiting_for_duration_input)
    await callback_query.message.answer(
        f"Отлично! ✅\n\n"  # TODO: Move duplicated message to the templates. (commands/exercise.py:94)
        f" {html.bold("Шаг 4:")} Теперь введите продолжительность выполнения упражнения. Например, {html.bold('1m')} для 1 минуты или {html.bold('30s')} для 30 секунд:"
    )
    await callback_query.answer()


@router.callback_query(
    StateFilter(StartWorkoutStates.workout_in_progress, StartWorkoutStates.paused),
    SkipWorkoutExerciseCallback.filter(),
)
async def skip_workout_exercise(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(StartWorkoutStates.skipping_exercise)
    await callback_query.answer()
