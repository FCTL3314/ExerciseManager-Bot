import asyncio

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import (
    WorkoutsSelectCallback,
    WorkoutsPaginationCallback,
    StartWorkoutCallback,
    PauseWorkoutCallback,
    ResumeWorkoutCallback,
)
from src.bot.enums import MessageAction
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.exercise import (
    create_active_workout_keyboard,
    create_paused_workout_keyboard,
)
from src.bot.keyboards.inline.workouts import (
    create_start_workout_keyboard,
)
from src.bot.services.exercise import handle_workout_exercise
from src.bot.services.shortcuts.message_templates import (
    ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
    ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
    NO_EXERCISES_MESSAGE,
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
    StartWorkoutStates.selecting_workout, WorkoutsSelectCallback.filter()
)
async def process_start_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    workout = await workout_service.retrieve(workout_id=callback_data.workout_id)

    if not workout.workout_exercises:
        await callback_query.message.answer(NO_EXERCISES_MESSAGE)
        await callback_query.answer()
        return

    workout_state = await workout_service.create_serialized_workout_state(workout)

    await state.update_data(**workout_state.model_dump())
    await state.set_state(StartWorkoutStates.workout_in_progress)

    await callback_query.message.edit_text(
        f"💪 Вы выбрали тренировку: {html.bold(workout.name)}!\n\n"
        f"🔹 Тренировка состоит из {html.bold(workout.exercises_count)} упражнений.\n"
        f"🔹 Приблизительное время тренировки - {html.bold(workout.get_humanized_workout_duration("ru"))}.",  # TODO: Change to i18n.current_locale
        reply_markup=await create_start_workout_keyboard(),
    )
    await callback_query.answer()


@router.callback_query(
    StartWorkoutStates.workout_in_progress, StartWorkoutCallback.filter()
)
async def process_start_workout(
    callback_query: CallbackQuery,
    callback_data: StartWorkoutCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await state.update_data(manual_mode_enabled=callback_data.manual_mode_enabled)
    await callback_query.answer()
    asyncio.create_task(
        handle_workout_exercise(callback_query.message, workout_service, state)
    )


@router.callback_query(
    StartWorkoutStates.workout_in_progress, PauseWorkoutCallback.filter()
)
async def process_pause_workout(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(StartWorkoutStates.paused)
    await callback_query.message.edit_reply_markup(
        reply_markup=await create_paused_workout_keyboard()
    )
    await callback_query.answer()


@router.callback_query(StartWorkoutStates.paused, ResumeWorkoutCallback.filter())
async def process_resume_workout(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await state.set_state(StartWorkoutStates.workout_in_progress)
    await callback_query.message.edit_reply_markup(
        reply_markup=await create_active_workout_keyboard()
    )
    await callback_query.answer()
