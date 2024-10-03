from typing import List, TypeVar, Generic, Union, Callable, Any, Optional

from starlette.responses import JSONResponse

# Define a generic type variable
T = TypeVar('T')
R = TypeVar('R')


class Pagination(Generic[T]):
    def __init__(self, items: List[T], total_items: int, current_page: int, total_pages: int):
        self.items = items  # List of items on the current page
        self.total_items = total_items  # Total number of items matching the criteria
        self.current_page = current_page  # Current page number
        self.total_pages = total_pages  # Total number of pages

    def __repr__(self) -> str:
        return (
            f"Pagination("
            f"items={self.items}, "
            f"total_items={self.total_items}, "
            f"current_page={self.current_page}, "
            f"total_pages={self.total_pages})"
        )

    def get_one(self) -> Union[T, None]:
        return self.items[0] if self.items else None

    def is_empty(self):
        return len(self.items) == 0

    def map_each(self, func: Callable[[T], Any]) -> None:
        """
        Applies the given function to each item in the `items` list.
        The function can modify the items in place or perform some action on them.
        """
        self.items = [func(item) for item in self.items]


class PaginatedResponse(Generic[R], JSONResponse):
    def __init__(self, pagination: Pagination[R], map_func: Optional[Callable[[R], Any]] = None, status: str = "OK", *args, **kwargs):
        if map_func:
            pagination.map_each(map_func)

        content = {
            "status": status,
            "items": pagination.items,
            "total_items": pagination.total_items,
            "current_page": pagination.current_page,
            "total_pages": pagination.total_pages
        }

        super().__init__(content=content, *args, **kwargs)
