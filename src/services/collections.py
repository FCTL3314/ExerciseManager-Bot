from typing import Any


def chunk_list(_list: list[Any], chunk_size: int) -> list[Any]:
    return [_list[i : i + chunk_size] for i in range(0, len(_list), chunk_size)]
