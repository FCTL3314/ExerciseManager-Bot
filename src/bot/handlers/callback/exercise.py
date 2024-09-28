from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.callbacks import NextExerciseCallback
from src.bot.handlers.callback import router
from src.bot.services.exercise import handle_workout_exercise
from src.bot.states.workout import StartWorkoutStates
from src.services.business.workouts import WorkoutServiceProto


@router.callback_query(StartWorkoutStates.doing_workout, NextExerciseCallback.filter())
async def process_next_exercise(
    callback_query: CallbackQuery,
    state: FSMContext,
    workout_service: WorkoutServiceProto,
) -> None:
    await callback_query.answer()
    await handle_workout_exercise(callback_query.message, workout_service, state)
