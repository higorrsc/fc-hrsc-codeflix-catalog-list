from abc import ABC, abstractmethod
from enum import StrEnum
from typing import List, Optional

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src.category import Category


class SortDirection(StrEnum):
    """
    Enum representing the sort direction for category searches.
    This enum defines two possible values: ASC for ascending order and DESC for descending order.
    """

    ASC = "asc"
    DESC = "desc"


class CategoryRepository(ABC):
    """
    Abstract base class for category repositories.
    This class defines the interface for category repositories, including methods
    for creating, updating, deleting, retrieving, and searching categories.
    """

    @abstractmethod
    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> List[Category]:
        """
        Searches for categories based on the given filters.

        Args:
            page (int): The page to be returned. Defaults to 1.
            per_page (int): The number of items per page. Defaults to 5.
            search (str | None): The search query. Defaults to None.
            sort (str | None): The name of the field to sort by. Defaults to None.
            direction (SortDirection): The sort direction. Defaults to ASC.

        Returns:
            List[Category]: A list of categories.
        """

        raise NotImplementedError("Method 'search' must be implemented by subclasses.")
