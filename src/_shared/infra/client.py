from abc import ABC, abstractmethod
from uuid import UUID

from src._shared.models.video import VideoResponse


class CodeflixClient(ABC):
    """
    Abstract base class for a codeflix client.
    """

    @abstractmethod
    def get_video(self, video_id: UUID) -> VideoResponse:
        """
        Retrieves a video by id.

        Args:
            video_id (UUID): The ID of the video to be retrieved.

        Returns:
            VideoResponse: The video response object containing the video details.
        """

        raise NotImplementedError
