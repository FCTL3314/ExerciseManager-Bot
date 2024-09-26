from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback, WorkoutsPageCallback
from src.bot.handlers.callback import router
from src.bot.keyboards.inline.workouts import get_workouts_keyboard
from src.bot.services.shortcuts.commands import ADD_WORKOUT_COMMAND
from src.bot.states import ExerciseAddingStates
from src.config import Settings
from src.services.business.workouts import IWorkoutService
from src.services.exceptions import NoWorkoutsError


@router.callback_query(WorkoutsPageCallback.filter())
async def process_workout_pagination(
    callback_query: CallbackQuery,
    callback_data: WorkoutsPageCallback,
    state: FSMContext,
    workout_service: IWorkoutService,
    settings: Settings,
) -> None:
    limit = settings.pagination.workout.workouts_keyboard_paginate_by
    offset = (callback_data.page - 1) * limit

    try:
        keyboard = await get_workouts_keyboard(
            user_id=callback_query.from_user.id,
            workout_service=workout_service,
            limit=limit,
            offset=offset,
            current_page=callback_data.page,
        )
    except NoWorkoutsError:
        await callback_query.message.edit_text(
            f"❌ У вас пока нет созданных тренировок. Пожалуйста, создайте тренировку перед добавлением упражнений, используя команду {html.bold(ADD_WORKOUT_COMMAND)}."
        )
        await callback_query.answer()
        return

    await state.update_data(page=callback_data.page)
    await callback_query.message.edit_text(
        "📋 Выберите тренировку, к которой хотите добавить упражнение:",
        reply_markup=keyboard,
    )

    await callback_query.answer()


@router.callback_query(WorkoutsSelectCallback.filter())
async def process_add_exercise_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
    workout_service: IWorkoutService,
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
