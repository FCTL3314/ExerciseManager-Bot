from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback
from src.bot.handlers.callback import router
from src.bot.states import ExerciseAddingStates


@router.callback_query(WorkoutsSelectCallback.filter())
async def process_add_exercise_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
) -> None:
    await state.update_data(workout_id=callback_data.workout_id)
    await state.set_state(ExerciseAddingStates.waiting_for_name_input)
    await callback_query.message.edit_text("Введите название упражнения:")
