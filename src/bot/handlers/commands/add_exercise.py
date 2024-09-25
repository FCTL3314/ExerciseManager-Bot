from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.commands import router
from src.bot.keyboards.inline.workouts import get_workouts_keyboard
from src.bot.services.shortcuts.commands import (
    ADD_EXERCISE_COMMAND,
)
from src.bot.states import ExerciseAddingStates
from src.services.business.workouts import IWorkoutService


@router.message(Command(ADD_EXERCISE_COMMAND.name))
async def cmd_add_exercise(
    message: Message,
    state: FSMContext,
    workout_service: IWorkoutService,
) -> None:
    workouts = await workout_service.list(user_id=message.from_user.id)
    if not workouts:
        await message.answer(
            "У вас нет созданных тренировок. Создайте тренировку перед добавлением упражнений."
        )
        return

    keyboard = await get_workouts_keyboard(workouts)
    await message.answer(
        "Выберите тренировку, в которую хотите добавить упражнение:",
        reply_markup=keyboard,
    )
    await state.set_state(ExerciseAddingStates.workout)
