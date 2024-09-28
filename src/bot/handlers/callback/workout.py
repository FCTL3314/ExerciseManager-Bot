import asyncio
import base64
import pickle

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import (
    WorkoutsSelectCallback,
    WorkoutsPaginationCallback,
    StartWorkoutCallback,
)
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
from src.models.workout import WorkoutExercise
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
    keyboard = await get_start_workout_keyboard()

    serialized_workout_exercises = base64.b64encode(
        pickle.dumps(workout.workout_exercises)
    ).decode("utf-8")

    await state.update_data(
        current_workout_exercise_index=0,
        workout_exercises=serialized_workout_exercises,
    )
    await state.set_state(StartWorkoutStates.doing_workout)

    for workout_exercise in workout.workout_exercises:
        print(workout_exercise.exercise.duration)
        print(workout_exercise.break_time)

    await callback_query.message.edit_text(
        f"💪 Вы выбрали тренировку: {html.bold(workout.name)}!\n\n"
        f"🔹 Тренировка состоит из {workout.exercises_count} упражнений!\n"
        f"🔹 Приблизительное время тренировки - {round(workout.workout_duration.seconds / 60, 1)} минут!",
        reply_markup=keyboard,
    )


@router.callback_query(StartWorkoutStates.doing_workout, StartWorkoutCallback.filter())
async def process_workout_exercise(
    callback_query: CallbackQuery, state: FSMContext
) -> None:
    await callback_query.answer()

    data = await state.get_data()

    current_workout_exercise_index = data["current_workout_exercise_index"]
    workout_exercises = pickle.loads(base64.b64decode(data["workout_exercises"]))

    workout_exercise: WorkoutExercise = workout_exercises[
        current_workout_exercise_index
    ]

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
    break_timer_message_template = "⌛️ Отдыхайте ещё {seconds_left} секунд..."
    exercise_timer_message_template = (
        "⌛️ Выполняйте упражнение ещё {seconds_left} секунд..."
    )

    # TODO: Move constants to the settings
    WORKOUT_PRE_START_TIMER_SECONDS = 15
    IS_MANUAL_MODE_ENABLED = True

    break_seconds = (
        WORKOUT_PRE_START_TIMER_SECONDS
        if current_workout_exercise_index == 0
        else int(workout_exercise.break_time.total_seconds())
    )

    for i, seconds in enumerate(range(break_seconds, -1, -1)):
        if await state.get_state() != StartWorkoutStates.doing_workout:
            return
        if i == 0:
            timer_message = await callback_query.message.answer(
                break_timer_message_template.format(seconds_left=html.bold(seconds))
            )
            continue
        await timer_message.edit_text(  # noqa
            break_timer_message_template.format(seconds_left=html.bold(seconds))
        )
        await asyncio.sleep(1)

    for seconds in range(
        int(workout_exercise.exercise.duration.total_seconds()), -1, -1
    ):
        if await state.get_state() != StartWorkoutStates.doing_workout:
            return
        await timer_message.edit_text(
            exercise_timer_message_template.format(seconds_left=html.bold(seconds))
        )
        await asyncio.sleep(1)

    await timer_message.edit_text(
        f"✅ Упражнение {html.bold(workout_exercise.exercise.name)} выполнено!"
    )

    if current_workout_exercise_index + 1 >= len(workout_exercises):
        await state.clear()
        await callback_query.message.answer("🎉 Тренировка закончена, ты молодец!")
        return

    await state.update_data(
        current_workout_exercise_index=current_workout_exercise_index + 1
    )

    if IS_MANUAL_MODE_ENABLED:
        keyboard = await get_start_workout_keyboard(
            text="➡️ Перейти к следующему упражнению"
        )
        await timer_message.edit_reply_markup(reply_markup=keyboard)
    else:
        await process_workout_exercise(callback_query, state)
