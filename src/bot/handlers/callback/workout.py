from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback, WorkoutsPaginationCallback
from src.bot.enums import MessageAction
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.workouts import get_start_workout_keyboard
from src.bot.message_templates import (
    ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
    ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
)
from src.bot.services.workout import send_select_workout_keyboard_or_error_message
from src.bot.states.workout import ExerciseAddingStates, StartWorkoutStates
from src.config import Settings
from src.services.business.workouts import WorkoutServiceProto


@router.callback_query(WorkoutsPaginationCallback.filter())
async def process_workout_pagination(
    callback_query: CallbackQuery,
    callback_data: WorkoutsPaginationCallback,
    workout_service: WorkoutServiceProto,
    settings: Settings,
) -> None:
    await send_select_workout_keyboard_or_error_message(
        text=ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
        no_workouts_message=ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
        message=callback_query.message,
        user_id=callback_query.from_user.id,
        workout_service=workout_service,
        limit=settings.pagination.workout.workouts_keyboard_paginate_by,
        offset=callback_data.offset,
        buttons_per_row=settings.pagination.workout.workouts_keyboard_buttons_per_row,
        message_action=MessageAction.edit,
        show_loading_message=False,
    )


@router.callback_query(
    ExerciseAddingStates.waiting_for_workout_selection, WorkoutsSelectCallback.filter()
)
async def process_add_exercise_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await state.update_data(workout_id=callback_data.workout_id)

    workout = await workout_service.retrieve(workout_id=callback_data.workout_id)

    await state.set_state(ExerciseAddingStates.waiting_for_name_input)
    await callback_query.message.edit_text(
        f"📋 Вы выбрали тренировку: {html.bold(workout.name)}.\n\n"
        "📝 Теперь давайте добавим новое упражнение.\n\n"
        f"🔹 {html.bold("Шаг 1:")} Введите название упражнения.\n"
        f"Например: {html.bold("Отжимания")}, {html.bold("Приседания")} или {html.bold("Планка")}."
    )


@router.callback_query(
    StartWorkoutStates.waiting_for_workout_selection, WorkoutsSelectCallback.filter()
)
async def process_start_workout_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await state.update_data(current_workout_id=callback_data.workout_id)

    workout = await workout_service.retrieve(workout_id=callback_data.workout_id)
    keyboard = await get_start_workout_keyboard()

    await state.set_state(StartWorkoutStates.doing_workout)
    await callback_query.message.edit_text(
        f"💪 Вы выбрали тренировку: {html.bold(workout.name)}!\n\n"
        f"🔹 Тренировка состоит из {workout.exercises_count} упражнений!\n"
        f"🔹 Приблизительное время тренировки - {workout.workout_duration.seconds // 60} минут!",
        reply_markup=keyboard,
    )
