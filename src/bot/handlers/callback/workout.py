from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback, WorkoutsPaginationCallback
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.workouts import get_workouts_keyboard
from src.bot.message_templates import NO_WORKOUTS_MESSAGE, SELECT_WORKOUT_MESSAGE
from src.bot.states import ExerciseAddingStates
from src.config import Settings
from src.services.business.workouts import WorkoutServiceProto
from src.services.exceptions import NoWorkoutsError


@router.callback_query(WorkoutsPaginationCallback.filter())
async def process_workout_pagination(
    callback_query: CallbackQuery,
    callback_data: WorkoutsPaginationCallback,
    workout_service: WorkoutServiceProto,
    settings: Settings,
) -> None:
    try:
        keyboard = await get_workouts_keyboard(
            user_id=callback_query.from_user.id,
            workout_service=workout_service,
            limit=settings.pagination.workout.workouts_keyboard_paginate_by,
            offset=callback_data.offset,
            buttons_per_row=settings.pagination.workout.workouts_keyboard_buttons_per_row,
        )
    except NoWorkoutsError:
        await callback_query.message.edit_text(NO_WORKOUTS_MESSAGE)
        return

    await callback_query.message.edit_text(
        SELECT_WORKOUT_MESSAGE, reply_markup=keyboard
    )


@router.callback_query(WorkoutsSelectCallback.filter())
async def process_add_exercise_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await state.update_data(workout_id=callback_data.workout_id)
    await state.set_state(ExerciseAddingStates.waiting_for_name_input)

    workout = await workout_service.retrieve(workout_id=callback_data.workout_id)

    await callback_query.message.edit_text(
        f"📋 Вы выбрали тренировку: {html.bold(workout.name)}.\n\n"
        "📝 Теперь давайте добавим новое упражнение.\n\n"
        f"🔹 {html.bold("Шаг 1:")} Введите название упражнения.\n"
        f"Например: {html.bold("Отжимания")}, {html.bold("Приседания")} или {html.bold("Планка")}."
    )

    await callback_query.answer()
