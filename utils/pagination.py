from typing import List, TypeVar, Generic, Union

# Define a generic type variable
T = TypeVar('T')


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
