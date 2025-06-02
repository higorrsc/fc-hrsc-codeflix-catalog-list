from uuid import UUID

from pydantic import HttpUrl

from src._shared.domain.entity import Entity
from src._shared.models.enums import Rating


class Video(Entity):
    """
    Represents a category in the system.
    This class inherits from Entity and includes additional fields
    specific to a genre.
    """

    title: str
    launch_year: int
    rating: Rating
    categories: set[UUID]
    cast_members: set[UUID]
    genres: set[UUID]
    banner: HttpUrl
