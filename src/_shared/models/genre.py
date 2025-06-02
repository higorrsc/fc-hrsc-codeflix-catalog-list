from uuid import UUID

from pydantic import BaseModel


class GenreResponse(BaseModel):
    """
    A Pydantic model representing a genre response.
    """

    id: UUID
    name: str
