from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    limit: int
    offset: int
    results: list[T]

    @property
    def total_pages(self) -> int:
        return (self.count + self.limit - 1) // self.limit
