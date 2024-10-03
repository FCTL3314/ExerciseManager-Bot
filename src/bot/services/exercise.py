from typing import Callable, Awaitable, Any

from aiogram import html
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.inline.exercise import (
    create_active_workout_keyboard,
)
from src.bot.keyboards.inline.workouts import (
    create_next_exercise_keyboard,
)
from src.bot.services.messages import send_message_by_file_type, run_timer
from src.bot.services.shortcuts.message_templates import (
    REST_PERIOD_TIMER_MESSAGE,
    WORKOUT_EXERCISE_TIMER_MESSAGE,
    EXERCISE_DESCRIPTION_MESSAGE,
    EXERCISE_COMPLETED_MESSAGE,
    WORKOUT_COMPLETED_MESSAGE,
    FAILED_TO_SEND_EXERCISE_IMAGE_MESSAGE,
)
from src.bot.states.workout import StartWorkoutStates
from src.services.business.workouts import WorkoutServiceProto


async def handle_workout_exercise(
    message: Message,
    workout_service: WorkoutServiceProto,
    state: FSMContext,
) -> None:
    data = await state.get_data()

    workout_settings = await workout_service.get_workout_settings(data)
    workout_state = await workout_service.get_current_workout_state(data)
    break_seconds = await workout_service.get_break_seconds(
        workout_state, workout_settings
    )
    workout_exercise = workout_state.current_workout_exercise

    exercise_text = EXERCISE_DESCRIPTION_MESSAGE.format(
        name=workout_exercise.exercise.name,
        description=workout_exercise.exercise.description or "",
        duration=workout_exercise.exercise.get_humanized_duration(
            "ru"
        ),  # TODO: Replace with i18n.current_locale
    )

    if workout_exercise.exercise.image:
        try:
            await send_message_by_file_type(
                message,
                workout_exercise.exercise.image,
                caption=exercise_text,
            )
        except TelegramBadRequest:
            await message.answer(FAILED_TO_SEND_EXERCISE_IMAGE_MESSAGE)
            await message.answer(exercise_text)
    else:
        await message.answer(exercise_text)

    timer_message: Message = await run_timer(
        break_seconds,
        on_tick=await get_on_tick(message, REST_PERIOD_TIMER_MESSAGE),
        on_stop=await get_on_stop(state),
        state=state,
        stop_states=(StartWorkoutStates.skipping_exercise, None),
        pause_states=(StartWorkoutStates.paused,),
    )

    timer_message: Message = await run_timer(
        int(workout_exercise.exercise.duration.total_seconds()),
        on_tick=await get_on_tick(
            message, WORKOUT_EXERCISE_TIMER_MESSAGE, timer_message
        ),
        on_stop=await get_on_stop(state),
        state=state,
        stop_states=(StartWorkoutStates.skipping_exercise, None),
        pause_states=(StartWorkoutStates.paused,),
    )

    if await state.get_state() is None:
        return

    await timer_message.edit_text(
        EXERCISE_COMPLETED_MESSAGE.format(name=workout_exercise.exercise.name)
    )

    if workout_state.no_more_exercises:
        await state.clear()
        await message.answer(WORKOUT_COMPLETED_MESSAGE)
        return

    await state.update_data(
        current_workout_exercise_index=workout_state.next_exercise_index
    )

    if workout_settings.manual_mode_enabled:
        await timer_message.edit_reply_markup(
            reply_markup=await create_next_exercise_keyboard()
        )
    else:
        await handle_workout_exercise(message, workout_service, state)


async def get_on_tick(
    message: Message,
    message_template: str,
    previous_message: Message | None = None,
) -> Callable[..., Awaitable[Any]]:
    async def on_tick(
        second: int, previous_tick_result: Message, *args, **kwargs
    ) -> Any:
        _previous_message = previous_tick_result

        if _previous_message is None:
            _previous_message = previous_message

        if _previous_message is None:
            return await message.answer(
                message_template.format(seconds_left=html.bold(second)),
                reply_markup=await create_active_workout_keyboard(),
            )

        return await _previous_message.edit_text(
            message_template.format(seconds_left=html.bold(second)),
            reply_markup=_previous_message.reply_markup,
        )

    return on_tick


async def get_on_stop(state: FSMContext) -> Callable[..., Awaitable[None]]:
    async def on_stop(*args, **kwargs) -> None:
        if await state.get_state() in (
            StartWorkoutStates.skipping_exercise,
            StartWorkoutStates.paused,
        ):
            await state.set_state(StartWorkoutStates.workout_in_progress)

    return on_stop
