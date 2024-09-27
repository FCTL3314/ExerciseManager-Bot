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

    @property
    def current_page(self) -> int:
        return (self.offset // self.limit) + 1

    @property
    def previous_offset(self) -> int:
        previous_page = self.current_page - 1
        if previous_page < 1:
            return 0
        return (previous_page - 1) * self.limit

    @property
    def next_offset(self) -> int:
        next_page = self.current_page + 1
        if next_page > self.total_pages:
            return self.offset
        return (next_page - 1) * self.limit

    @property
    def has_previous(self) -> bool:
        return self.current_page > 1

    @property
    def has_next(self) -> bool:
        return self.current_page < self.total_pages