import asyncio
from typing import Callable, Any, Awaitable


async def run_timer(
    seconds: int,
    on_tick: Callable[..., Awaitable[Any]],
    should_continue: Callable[..., Awaitable[bool]],
    previous_response: Any = None,
) -> Any:
    for i, second in enumerate(range(seconds, -1, -1)):
        if not await should_continue(
            iteration=i, second=second, previous_response=previous_response
        ):
            break

        previous_response = await on_tick(
            iteration=i, second=second, previous_response=previous_response
        )

        await asyncio.sleep(1)

    return previous_response
