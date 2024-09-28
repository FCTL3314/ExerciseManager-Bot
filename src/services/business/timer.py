import asyncio
from typing import Callable, Any, Awaitable


async def run_timer(
    seconds: int,
    on_tick: Callable[..., Awaitable[Any]],
    should_continue: Callable[..., Awaitable[bool]] | None = None,
    previous_response: Any = None,
) -> Any:
    for i, second in enumerate(range(seconds, -1, -1)):
        kwargs = {
            "iteration": i,
            "second": second,
            "previous_response": previous_response,
        }

        if should_continue is not None and not await should_continue(**kwargs):
            break

        previous_response = await on_tick(**kwargs)

        await asyncio.sleep(1)

    return previous_response
