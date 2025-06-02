from typing import List
from uuid import UUID

from pydantic import BaseModel

from src._shared.models.banner import BannerResponse
from src._shared.models.cast_member import CastMemberResponse
from src._shared.models.category import CategoryResponse
from src._shared.models.enums import Rating
from src._shared.models.genre import GenreResponse


class VideoResponse(BaseModel):
    """
    A Pydantic model representing a video response.
    """

    id: UUID
    title: str
    launch_year: int
    rating: Rating
    is_active: bool
    categories: List[CategoryResponse]
    cast_members: List[CastMemberResponse]
    genres: List[GenreResponse]
    banner: BannerResponse
