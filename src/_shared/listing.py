from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel, Field

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.domain.entity import Entity


class SortDirection(StrEnum):
    """
    Enum representing the sort direction for  searches.
    This enum defines two possible values: ASC for ascending order and DESC for descending order.
    """

    ASC = "asc"
    DESC = "desc"


class ListInput[SortableFieldsType: StrEnum](BaseModel):
    """
    Input class for List use case.
    """

    page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    sort: Optional[SortableFieldsType] = None
    direction: SortDirection = SortDirection.ASC
    search: Optional[str] = None


class ListOutputMeta(BaseModel):
    """
    Meta class for List use case.
    """

    page: int = 1
    per_page: int = DEFAULT_PAGINATION_SIZE
    sort: Optional[str] = None
    direction: SortDirection = SortDirection.ASC


class ListOutput[T: Entity](BaseModel):
    """
    Output class for List use case.
    """

    data: List[T] = Field(default_factory=list)
    meta: ListOutputMeta = Field(default_factory=ListOutputMeta)
