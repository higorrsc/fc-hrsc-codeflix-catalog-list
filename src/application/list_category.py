from enum import StrEnum
from typing import Optional

from src._shared.application.list_entity import ListEntity
from src._shared.listing import ListInput
from src.domain.category import Category


class CategorySortableFields(StrEnum):
    """
    Enum representing sortable fields for the List use case.
    """

    NAME = "name"
    DESCRIPTION = "description"


class ListCategoryInput(ListInput[CategorySortableFields]):
    """
    Input class for the ListCategory use case.
    """

    sort: Optional[CategorySortableFields] = CategorySortableFields.NAME


class ListCategory(ListEntity[Category]):
    """
    Use case for listing categories.

    This class provides functionality to list categories based on various filters such
    as pagination, sorting, and searching.

    It interacts with the CategoryRepository to retrieve the categories and returns them
    in a structured format.
    """
