from abc import ABC

from src._shared.domain.repository import Repository
from src.domain.cast_member import CastMember


class CastMemberRepository(Repository[CastMember], ABC):
    """
    CastMemberRepository interface for interacting with categories in the database.
    """
