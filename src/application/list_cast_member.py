from enum import StrEnum
from typing import Optional

from src._shared.application.list_entity import ListEntity
from src._shared.listing import ListInput
from src.domain.cast_member import CastMember


class CastMemberSortableFields(StrEnum):
    """
    Enum representing sortable fields for the List use case.
    """

    NAME = "name"
    TYPE = "type"


class ListCastMemberInput(ListInput[CastMemberSortableFields]):
    """
    Input class for the ListCastMember use case.
    """

    sort: Optional[CastMemberSortableFields] = CastMemberSortableFields.NAME


class ListCastMember(ListEntity[CastMember]):
    """
    Use case for listing categories.

    This class provides functionality to list categories based on various filters such
    as pagination, sorting, and searching.

    It interacts with the CategoryRepository to retrieve the categories and returns them
    in a structured format.
    """
