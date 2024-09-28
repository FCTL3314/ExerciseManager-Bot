import asyncio
import base64
import pickle

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import (
    WorkoutsSelectCallback,
    WorkoutsPaginationCallback,
    NextExerciseCallback,
)
from src.bot.enums import MessageAction
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.workouts import get_next_exercise_keyboard
from src.bot.services.shortcuts.message_templates import (
    ADD_EXERCISE_NO_WORKOUTS_MESSAGE,
    ADD_EXERCISE_WORKOUT_SELECTION_MESSAGE,
    REST_PERIOD_TIMER_MESSAGE,
    WORKOUT_EXERCISE_TIMER_MESSAGE,
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
async def process_start_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    workout = await workout_service.retrieve(workout_id=callback_data.workout_id)
    keyboard = await get_next_exercise_keyboard(text="🚀 Начать тренировку")

    serialized_workout_exercises = base64.b64encode(
        pickle.dumps(workout.workout_exercises)
    ).decode("utf-8")

    await state.update_data(workout_exercises=serialized_workout_exercises)
    await state.set_state(StartWorkoutStates.doing_workout)

    await callback_query.message.edit_text(
        f"💪 Вы выбрали тренировку: {html.bold(workout.name)}!\n\n"
        f"🔹 Тренировка состоит из {workout.exercises_count} упражнений.\n"
        f"🔹 Приблизительное время тренировки - {workout.get_humanized_workout_duration("ru")}.",  # TODO: Change to i18n.current_locale
        reply_markup=keyboard,
    )


@router.callback_query(StartWorkoutStates.doing_workout, NextExerciseCallback.filter())
async def process_workout_exercise(
    callback_query: CallbackQuery,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await callback_query.answer()
    data = await state.get_data()

    workout_settings = await workout_service.get_workout_settings()
    workout_state = await workout_service.get_current_workout_state(data)
    workout_exercise = workout_state.current_workout_exercise

    if workout_exercise.exercise.image:
        await callback_query.message.answer_photo(
            photo=workout_exercise.exercise.image,
            caption=f"{html.bold(workout_exercise.exercise.name)}\n"
            f"{workout_exercise.exercise.description}\n",
        )
    else:
        await callback_query.message.answer(
            f"{html.bold(workout_exercise.exercise.name)}\n"
            f"{workout_exercise.exercise.description}\n",
        )

    # Start: Generate break seconds
    break_seconds = (
        workout_settings.pre_start_timer_seconds
        if workout_state.is_first_exercise
        else int(workout_exercise.break_time.total_seconds())
    )
    # End

    # Start: Start timer message
    for i, seconds in enumerate(range(break_seconds, -1, -1)):
        if await state.get_state() != StartWorkoutStates.doing_workout:
            return
        if i == 0:
            timer_message = await callback_query.message.answer(
                REST_PERIOD_TIMER_MESSAGE.format(seconds_left=html.bold(seconds))
            )
            continue
        await timer_message.edit_text(  # noqa
            REST_PERIOD_TIMER_MESSAGE.format(seconds_left=html.bold(seconds))
        )
        await asyncio.sleep(1)

    for seconds in range(
        int(workout_exercise.exercise.duration.total_seconds()), -1, -1
    ):
        if await state.get_state() != StartWorkoutStates.doing_workout:
            return
        await timer_message.edit_text(
            WORKOUT_EXERCISE_TIMER_MESSAGE.format(seconds_left=html.bold(seconds))
        )
        await asyncio.sleep(1)
    # End

    await timer_message.edit_text(
        f"✅ Упражнение {html.bold(workout_exercise.exercise.name)} выполнено!"
    )

    # Start: Is workout finished | Is no more exercises
    if workout_state.no_more_exercises:
        await state.clear()
        await callback_query.message.answer("🎉 Тренировка закончена, ты молодец!")
        return
    # End

    await state.update_data(
        current_workout_exercise_index=workout_state.next_exercise_index
    )

    if workout_settings.manual_mode_enabled:
        keyboard = await get_next_exercise_keyboard(
            text="➡️ Перейти к следующему упражнению"
        )
        await timer_message.edit_reply_markup(reply_markup=keyboard)
        return

    await process_workout_exercise(callback_query, state)
