from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src.category import Category
from src.category_repository import CategoryRepository, SortDirection


class SortableFields(StrEnum):
    """
    Enum representing sortable fields for the ListCategory use case.
    """

    NAME = "name"
    DESCRIPTION = "description"


class ListCategoryInput(BaseModel):
    """
    Input class for ListCategory use case.
    """

    page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    sort: SortableFields = SortableFields.NAME
    direction: SortDirection = SortDirection.ASC
    search: Optional[str] = None


class ListCategoryOutputMeta(BaseModel):
    """
    Meta class for ListCategory use case.
    """

    page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    sort: Optional[str] = None
    direction: SortDirection = SortDirection.ASC


class ListCategoryOutput(BaseModel):
    """
    Output class for ListCategory use case.
    """

    data: List[Category]
    meta: ListCategoryOutputMeta


class ListCategory:
    """
    Use case for listing categories.

    This class provides functionality to list categories based on various filters such
    as pagination, sorting, and searching.

    It interacts with the CategoryRepository to retrieve the categories and returns them
    in a structured format.
    """

    def __init__(self, repository: CategoryRepository) -> None:
        """
        Initializes a new instance of the ListCategory class.

        Args:
            repository (CategoryRepository): The category repository to use.
        """

        self._repository = repository

    def execute(self, params: ListCategoryInput) -> ListCategoryOutput:
        """
        Executes the ListCategory use case.

        This method takes an input of type ListCategoryInput and returns an output
        of type ListCategoryOutput.
        It uses the provided CategoryRepository to search for categories based on the given filters.
        The search query is delegated to the CategoryRepository, which returns a list of categories.
        The method then maps the list of categories to ListCategoryOutput and returns it.

        Args:
            params (ListCategoryInput): The input for the ListCategory use case.

        Returns:
            ListCategoryOutput: The output for the ListCategory use case.
        """
        categories = self._repository.search(
            page=params.page,
            per_page=params.per_page,
            sort=params.sort.value,
            direction=params.direction,
            search=params.search,
        )

        return ListCategoryOutput(
            data=categories,
            meta=ListCategoryOutputMeta(
                page=params.page,
                per_page=params.per_page,
                sort=params.sort.value,
                direction=params.direction,
            ),
        )
