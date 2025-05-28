from enum import StrEnum

from src._shared.domain.entity import Entity


class CastMemberType(StrEnum):
    """
    Enumeration of cast member types.
    """

    ACTOR = "actor"
    DIRECTOR = "director"


class CastMember(Entity):
    """
    Represents a cast member in the system.
    """

    name: str
    type: CastMemberType
