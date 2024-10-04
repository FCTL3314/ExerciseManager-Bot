import asyncio
import time
from typing import Iterable, Callable

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message
from mypy.semanal_shared import Protocol
from typing_extensions import TypeVar, Generic

from src.bot.keyboards.inline.exercise import create_active_workout_keyboard
from src.bot.states.workout import StartWorkoutStates
from src.constants import MIN_TIMER_MESSAGE_SECONDS_INTERVAL

T = TypeVar("T")


class TimerOnTickCallbackProto(Generic[T]):

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: T
    ) -> T: ...


class TimerOnStopCallbackProto(Generic[T]):

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: T
    ) -> T: ...


class TimerProto(Protocol[T]):

    async def run_timer(self) -> T: ...


class AiogramTimerProto(Protocol[T]):

    async def run_timer(
        self,
        seconds: int,
        tick_callback: TimerOnTickCallbackProto[Message],
        stop_states: Iterable[StatesGroup] = None,
        pause_states: Iterable[StatesGroup] = None,
        stop_callback: TimerOnStopCallbackProto | None = lambda: ...,
    ) -> T: ...


class AiogramMessageTimer(AiogramTimerProto[Message]):
    def __init__(self, state: FSMContext) -> None:
        self._state = state

    async def run_timer(
        self,
        seconds: int,
        tick_callback: TimerOnTickCallbackProto[Message],
        stop_states: Iterable[StatesGroup] = None,
        pause_states: Iterable[StatesGroup] = None,
        stop_callback: TimerOnStopCallbackProto = lambda: ...,
    ) -> Message:
        if seconds <= 0:
            raise ValueError("seconds must be a positive integer")

        previous_tick_result = None
        remaining_seconds = seconds
        iteration_num = 0

        while remaining_seconds >= 0:
            kwargs = {
                "iteration_num": iteration_num,
                "second": remaining_seconds,
                "previous_tick_result": previous_tick_result,
            }

            current_state = await self._state.get_state()

            if stop_states and current_state in stop_states:
                await stop_callback(**kwargs)
                return previous_tick_result

            if pause_states and current_state in pause_states:
                while await self._state.get_state() in pause_states:
                    await asyncio.sleep(1)

            start_time = time.monotonic()
            previous_tick_result = await tick_callback(**kwargs)
            end_time = time.monotonic()

            elapsed_time = end_time - start_time
            remaining_seconds -= int(elapsed_time)

            remaining_sleep_time = 1 - (elapsed_time % 1)

            if remaining_sleep_time > 0 and remaining_seconds > 0:
                await asyncio.sleep(remaining_sleep_time)

            remaining_seconds -= 1
            iteration_num += 1

        await stop_callback(**kwargs)  # noqa
        return previous_tick_result


class WorkoutTimerOnTickCallback(TimerOnTickCallbackProto[Message]):

    def __init__(
        self,
        message: Message,
        total_seconds: int,
        message_template: str = None,
        progress_bar_generator: Callable[[int], str] | None = None,
        message_to_start_with: Message | None = None,
    ) -> None:
        self._message = message
        self._total_seconds = total_seconds
        self._message_template = message_template
        self._progress_bar_generator = progress_bar_generator
        self._message_to_start_with = message_to_start_with

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: Message
    ) -> Message:
        if iteration_num == 0:
            _previous_message = self._message_to_start_with
        else:
            _previous_message = previous_tick_result

        if iteration_num != 0 and second % MIN_TIMER_MESSAGE_SECONDS_INTERVAL != 0:
            return _previous_message

        if self._progress_bar_generator is not None:
            progress = int(((self._total_seconds - second) / self._total_seconds) * 100)
            progress = min(max(progress, 0), 100)

            text = self._progress_bar_generator(progress)
        else:
            text = self._message_template.format(seconds_left=second)

        if _previous_message is None:
            return await self._message.answer(
                text,
                reply_markup=await create_active_workout_keyboard(),
            )

        return await _previous_message.edit_text(
            text,
            reply_markup=_previous_message.reply_markup,
        )


class WorkoutTimerOnStopCallback(TimerOnStopCallbackProto[None]):

    def __init__(self, state: FSMContext) -> None:
        self._state = state

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: T
    ) -> None:
        if await self._state.get_state() in (
            StartWorkoutStates.skipping_exercise,
            StartWorkoutStates.paused,
        ):
            await self._state.set_state(StartWorkoutStates.workout_in_progress)
