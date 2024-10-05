from mypy.semanal_shared import Protocol
from typing_extensions import TypeVar, Generic

T = TypeVar("T")


class SchedulerCallbackProto(Generic[T]):

    async def __call__(
        self, iteration_num: int, second: int, previous_tick_result: T
    ) -> T: ...


class SchedulerProto(Protocol[T]):

    async def run_timer(self) -> T: ...
