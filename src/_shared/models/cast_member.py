from uuid import UUID

from pydantic import BaseModel


class CastMemberResponse(BaseModel):
    """
    A Pydantic model representing a cast member response.
    """

    id: UUID
    name: str
    type: str
