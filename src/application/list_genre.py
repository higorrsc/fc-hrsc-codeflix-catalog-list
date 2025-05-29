from enum import StrEnum
from typing import Optional

from src._shared.application.list_entity import ListEntity
from src._shared.listing import ListInput
from src.domain.genre import Genre


class GenreSortableFields(StrEnum):
    """
    Enum representing sortable fields for the List use case.
    """

    NAME = "name"


class ListGenreInput(ListInput[GenreSortableFields]):
    """
    Input class for the ListGenre use case.
    """

    sort: Optional[GenreSortableFields] = GenreSortableFields.NAME


class ListGenre(ListEntity[Genre]):
    """
    Use case for listing genres.

    This class provides functionality to list genres based on various filters such
    as pagination, sorting, and searching.

    It interacts with the GenreRepository to retrieve the genres and returns them
    in a structured format.
    """
