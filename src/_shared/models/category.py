from uuid import UUID

from pydantic import BaseModel


class CategoryResponse(BaseModel):
    """
    A Pydantic model representing a category response.
    """

    id: UUID
    name: str
    description: str
