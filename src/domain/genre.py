from uuid import UUID

from src._shared.domain.entity import Entity


class Genre(Entity):
    """
    Represents a category in the system.
    This class inherits from Entity and includes additional fields
    specific to a genre.
    """

    name: str
    categories: set[UUID]
