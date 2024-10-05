# TODO: Simplify module

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards.inline.workouts import (
    create_next_exercise_keyboard,
)
from src.bot.services.messages import send_message_by_file_type
from src.bot.services.shortcuts.message_templates import (
    EXERCISE_DESCRIPTION_MESSAGE,
    EXERCISE_COMPLETED_MESSAGE,
    WORKOUT_COMPLETED_MESSAGE,
    FAILED_TO_SEND_EXERCISE_IMAGE_MESSAGE,
    WORKOUT_REST_TIMER_MESSAGE,
    get_workout_exercise_progress_bar,
)
from src.bot.states.workout import StartWorkoutStates
from src.services.business.workouts import WorkoutServiceProto
from src.bot.services.schedule import (
    AiogramMessageScheduler,
    EditWorkoutProgressMessageCallback,
    EditWorkoutTimerMessageCallback,
    ResetWorkoutStateCallback,
)


async def handle_workout_exercise(
    message: Message,
    workout_service: WorkoutServiceProto,
    state: FSMContext,
) -> None:
    data = await state.get_data()

    workout_settings = await workout_service.get_workout_settings(data)
    workout_state = await workout_service.get_current_workout_state(data)
    workout_exercise = workout_state.current_workout_exercise

    break_seconds = await workout_service.get_break_seconds(
        workout_state, workout_settings
    )
    exercise_duration = int(workout_exercise.exercise.duration.total_seconds())

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

    timer = AiogramMessageScheduler(state=state)

    timer_message = await timer.run_timer(
        seconds=break_seconds,
        tick_callback=EditWorkoutTimerMessageCallback(
            message=message,
            total_seconds=break_seconds,
            message_template=WORKOUT_REST_TIMER_MESSAGE,
        ),
        stop_callback=ResetWorkoutStateCallback(state=state),
        stop_states=(StartWorkoutStates.skipping_exercise, None),
        pause_states=(StartWorkoutStates.paused,),
    )

    timer_message = await timer.run_timer(
        seconds=exercise_duration,
        tick_callback=EditWorkoutProgressMessageCallback(
            message=message,
            total_seconds=exercise_duration,
            progress_bar_generator=get_workout_exercise_progress_bar,
            message_to_edit=timer_message,
        ),
        stop_callback=ResetWorkoutStateCallback(state=state),
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
