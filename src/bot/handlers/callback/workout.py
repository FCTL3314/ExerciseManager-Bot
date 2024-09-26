from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback
from src.bot.handlers.callback import router
from src.bot.states import ExerciseAddingStates
from src.services.business.workouts import IWorkoutService


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
