from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import WorkoutsSelectCallback
from src.bot.handlers.callback import router
from src.bot.states import ExerciseAddingStates


@router.callback_query(WorkoutsSelectCallback.filter())
async def process_workout_selection(
    callback_query: CallbackQuery,
    callback_data: WorkoutsSelectCallback,
    state: FSMContext,
) -> None:
    workout_id = callback_data.workout_id
    await state.update_data(workout_id=workout_id)
    await callback_query.message.edit_text("Введите название упражнения:")
    await state.set_state(ExerciseAddingStates.name)
    await callback_query.answer()
