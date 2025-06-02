from enum import StrEnum
from typing import Optional

from src._shared.application.list_entity import ListEntity
from src._shared.listing import ListInput
from src.domain.video import Video


class VideoSortableFields(StrEnum):
    """
    Enum representing sortable fields for the List use case.
    """

    TITLE = "title"


class ListVideoInput(ListInput[VideoSortableFields]):
    """
    Input class for the ListVideo use case.
    """

    sort: Optional[VideoSortableFields] = VideoSortableFields.TITLE


class ListVideo(ListEntity[Video]):
    """
    Use case for listing genres.

    This class provides functionality to list genres based on various filters such
    as pagination, sorting, and searching.

    It interacts with the VideoRepository to retrieve the genres and returns them
    in a structured format.
    """
