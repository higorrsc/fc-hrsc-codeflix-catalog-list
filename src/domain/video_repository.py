from abc import ABC, abstractmethod

from src._shared.domain.repository import Repository
from src.domain.video import Video


class VideoRepository(Repository[Video], ABC):
    """
    VideoRepository interface for interacting with videos in the database.
    """

    @abstractmethod
    def save(self, video: Video):
        """
        Saves a video to the database.

        Args:
            video (Video): The video to be saved.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """

        raise NotImplementedError
