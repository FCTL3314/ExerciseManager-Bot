from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

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
from src.services.business.timer import run_timer
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

    workout_state = await workout_service.create_serialized_workout_state(workout)

    await state.update_data(**workout_state.model_dump())
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
    break_seconds = await workout_service.get_break_seconds(
        workout_state, workout_settings
    )
    workout_exercise = workout_state.current_workout_exercise

    exercise_text = (
        f"{html.bold(workout_exercise.exercise.name)}\n"
        f"{workout_exercise.exercise.description}\n"
    )

    if workout_exercise.exercise.image:
        await callback_query.message.answer_photo(
            photo=workout_exercise.exercise.image,
            caption=exercise_text,
        )
    else:
        await callback_query.message.answer(exercise_text)

    async def get_on_tick(
        message_template: str,
    ) -> Callable[..., Awaitable[Any]]:
        async def on_tick(
            second: int, previous_response: Message, *args, **kwargs
        ) -> Any:
            if previous_response is None:
                return await callback_query.message.answer(
                    message_template.format(seconds_left=html.bold(second))
                )

            return await previous_response.edit_text(
                message_template.format(seconds_left=html.bold(second))
            )

        return on_tick

    async def should_continue(*args, **kwargs) -> bool:
        return await state.get_state() == StartWorkoutStates.doing_workout

    timer_message: Message = await run_timer(
        break_seconds,
        on_tick=await get_on_tick(REST_PERIOD_TIMER_MESSAGE),
        should_continue=should_continue,
    )

    timer_message: Message = await run_timer(
        int(workout_exercise.exercise.duration.total_seconds()),
        on_tick=await get_on_tick(WORKOUT_EXERCISE_TIMER_MESSAGE),
        should_continue=should_continue,
        previous_response=timer_message,
    )

    await timer_message.edit_text(
        f"✅ Упражнение {html.bold(workout_exercise.exercise.name)} выполнено!"
    )

    if workout_state.no_more_exercises:
        await state.clear()
        await callback_query.message.answer("🎉 Тренировка закончена, ты молодец!")
        return

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
