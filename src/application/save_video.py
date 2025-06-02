from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src._shared.infra.client import CodeflixClient
from src._shared.models.enums import Rating
from src._shared.models.video import VideoResponse
from src.domain.video import Video
from src.domain.video_repository import VideoRepository


class SaveVideoInput(BaseModel):
    """
    A Pydantic model representing the input for saving a video.
    """

    id: UUID
    title: str
    launch_year: int
    rating: Rating
    created_at: datetime
    updated_at: datetime
    is_active: bool


class SaveVideo:
    """
    Use case for saving a video.
    """

    def __init__(self, repository: VideoRepository, client: CodeflixClient) -> None:
        """
        Initializes a new instance of the SaveVideo class.

        Args:
            repository (VideoRepository): The video repository to use.
            client (CodeflixClient): The Codeflix client to use for retrieving a video.
        """

        self._repository = repository
        self._client = client

    def execute(self, video_input: SaveVideoInput) -> None:
        """
        Executes the SaveVideo use case.

        Args:
            video_input (SaveVideoInput): The video_input parameters for the use case.
        """

        http_data: VideoResponse = self._client.get_video(video_input.id)
        categories = {category.id for category in http_data.categories}
        cast_members = {cast_member.id for cast_member in http_data.cast_members}
        genres = {genre.id for genre in http_data.genres}
        banner_url = http_data.banner.raw_location

        video = Video(
            **video_input.model_dump(mode="python"),
            categories=categories,
            cast_members=cast_members,
            genres=genres,
            banner=banner_url,
        )

        self._repository.save(video)
