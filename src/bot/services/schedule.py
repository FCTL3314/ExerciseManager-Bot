import asyncio
import time
from abc import ABC, abstractmethod
from typing import Iterable, Callable, TypeVar, Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import Message
from typing_extensions import Protocol

from src.bot.keyboards.inline.exercise import create_active_workout_keyboard
from src.bot.states.workout import StartWorkoutStates
from src.constants import MIN_TIMER_MESSAGE_SECONDS_INTERVAL
from src.services.schedule import SchedulerCallbackProto

T = TypeVar("T")


class AiogramSchedulerProto(Protocol[T]):

    async def run_timer(
        self,
        seconds: int,
        tick_callback: SchedulerCallbackProto[Message],
        stop_states: Iterable[StatesGroup] = None,
        pause_states: Iterable[StatesGroup] = None,
        stop_callback: SchedulerCallbackProto[None] = lambda: ...,
    ) -> T: ...


class AiogramMessageScheduler(AiogramSchedulerProto[Message]):
    def __init__(self, state: FSMContext) -> None:
        self._state = state

    async def run_timer(
        self,
        seconds: int,
        tick_callback: SchedulerCallbackProto[Message],
        stop_states: Iterable[StatesGroup] | None = None,
        pause_states: Iterable[StatesGroup] | None = None,
        stop_callback: SchedulerCallbackProto[None] = lambda: ...,
    ) -> Message:
        if seconds <= 0:
            raise ValueError("seconds must be a positive integer")

        previous_tick_result = None
        remaining_seconds = seconds
        iteration_num = 0

        while remaining_seconds >= 0:
            kwargs = await self._get_kwargs(
                iteration_num, remaining_seconds, previous_tick_result
            )

            if await self._should_stop(stop_states):
                await stop_callback(**kwargs)
                return previous_tick_result

            while await self._should_pause(pause_states):
                await asyncio.sleep(1)

            start_time = time.monotonic()
            previous_tick_result = await tick_callback(**kwargs)
            end_time = time.monotonic()

            elapsed_time, rounded_elapsed_time, remaining_sleep_time = (
                await self._calculate_sleep_params(start_time, end_time)
            )
            remaining_seconds -= rounded_elapsed_time

            if await self._should_sleep(remaining_sleep_time, remaining_seconds):
                await asyncio.sleep(remaining_sleep_time)

            remaining_seconds -= 1
            iteration_num += 1

        await stop_callback(**kwargs)  # noqa
        return previous_tick_result

    @staticmethod
    async def _get_kwargs(
        iteration_num, remaining_seconds, previous_tick_result
    ) -> dict[str, Any]:
        return {
            "iteration_num": iteration_num,
            "second": remaining_seconds,
            "previous_tick_result": previous_tick_result,
        }

    async def _should_stop(self, stop_states: list[StatesGroup] | None) -> bool:
        return stop_states and await self._state.get_state() in stop_states

    async def _should_pause(self, pause_states: list[StatesGroup] | None) -> bool:
        return pause_states and await self._state.get_state() in pause_states

    @staticmethod
    async def _calculate_remaining_sleep_time(elapsed_time: float) -> float:
        return 1 - (elapsed_time % 1)

    async def _calculate_sleep_params(
        self, start_time: float, end_time: float
    ) -> tuple[float, int, float]:
        elapsed_time = end_time - start_time
        rounded_elapsed_time = int(elapsed_time)
        remaining_sleep_time = await self._calculate_remaining_sleep_time(elapsed_time)
        return elapsed_time, rounded_elapsed_time, remaining_sleep_time

    @staticmethod
    async def _should_sleep(
        remaining_sleep_time: float, remaining_seconds: float
    ) -> bool:
        return remaining_sleep_time > 0 and remaining_seconds > 0


class BaseEditWorkoutMessageCallback(SchedulerCallbackProto[Message], ABC):
    def __init__(
        self,
        message: Message,
        total_seconds: int,
        message_to_edit: Message | None = None,
    ) -> None:
        self._message = message
        self._total_seconds = total_seconds
        self._message_to_edit = message_to_edit

    async def _get_previous_message(
        self, iteration_num: int, previous_tick_result: Message
    ) -> Message:
        if iteration_num == 0:
            return self._message_to_edit
        return previous_tick_result

    @staticmethod
    async def should_edit(iteration_num: int, second: int) -> bool:
        return iteration_num == 0 or second % MIN_TIMER_MESSAGE_SECONDS_INTERVAL == 0

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: Message
    ) -> Message:
        previous_message = await self._get_previous_message(
            iteration_num, previous_tick_result
        )

        if not await self.should_edit(iteration_num, second):
            return previous_message

        text = self._generate_text(second)

        if previous_message is None:
            return await self._message.answer(
                text,
                reply_markup=await create_active_workout_keyboard(),
            )

        return await previous_message.edit_text(
            text,
            reply_markup=previous_message.reply_markup,
        )

    @abstractmethod
    def _generate_text(self, second: int) -> str: ...


class EditWorkoutProgressMessageCallback(BaseEditWorkoutMessageCallback):
    def __init__(
        self,
        message: Message,
        total_seconds: int,
        progress_bar_generator: Callable[[int], str],
        message_to_edit: Message | None = None,
    ) -> None:
        super().__init__(message, total_seconds, message_to_edit)
        self._progress_bar_generator = progress_bar_generator

    def _generate_text(self, second: int) -> str:
        progress = int(((self._total_seconds - second) / self._total_seconds) * 100)
        progress = min(max(progress, 0), 100)
        return self._progress_bar_generator(progress)


class EditWorkoutTimerMessageCallback(BaseEditWorkoutMessageCallback):
    def __init__(
        self,
        message: Message,
        total_seconds: int,
        message_template: str,
        message_to_edit: Message | None = None,
    ) -> None:
        super().__init__(message, total_seconds, message_to_edit)
        self._message_template = message_template

    def _generate_text(self, second: int) -> str:
        return self._message_template.format(seconds_left=second)


class ResetWorkoutStateCallback(SchedulerCallbackProto[None]):

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
