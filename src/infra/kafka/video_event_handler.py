import logging

from src._shared.infra.kafka.event_handler import AbstractEventHandler
from src.application.save_video import SaveVideo, SaveVideoInput
from src.domain.video import Rating
from src.infra.client.http_codeflix import HttpCodeflixClient
from src.infra.elasticsearch.elasticsearch_video_repository import (
    ElasticsearchVideoRepository,
)
from src.infra.kafka.parser import ParsedEvent

logger = logging.getLogger(__name__)


class VideoEventHandler(AbstractEventHandler):
    """
    Handles events related to videos.
    """

    def __init__(self, save_use_case: SaveVideo | None = None):
        """
        Initializes a new instance of the VideoEventHandler class.

        Args:
            save_use_case (SaveVideo, optional): The use case to be used for saving a video.
                Defaults to None, which will create a new instance of SaveVideo with the
                Elasticsearch repository and the HTTP Codeflix client.
        """

        self.save_use_case = save_use_case or SaveVideo(
            repository=ElasticsearchVideoRepository(),
            client=HttpCodeflixClient(),
        )

    def _handle_update_or_create(self, event: ParsedEvent) -> None:
        """
        Handles the update or creation of a video based on the parsed event.

        Args:
            event (ParsedEvent): The event containing the payload for the video to be saved.
        """

        video_input = SaveVideoInput(
            id=event.payload["id"],
            title=event.payload["title"],
            launch_year=event.payload["launch_year"],
            rating=Rating(event.payload["rating"]),
            created_at=event.payload["created_at"],
            updated_at=event.payload["updated_at"],
            is_active=event.payload["is_active"],
        )
        self.save_use_case.execute(video_input)

    def handle_created(self, event: ParsedEvent) -> None:
        """
        Handles the creation of a video based on the parsed event.

        Args:
            event (ParsedEvent): The event containing the payload for the video to be saved.
        """

        logger.info("Creating video with payload: %s", event.payload)
        self._handle_update_or_create(event)

    def handle_updated(self, event: ParsedEvent) -> None:
        """
        Handles the update of a video based on the parsed event.

        Args:
            event (ParsedEvent): The event containing the payload for the video to be updated.
        """

        logger.info("Updating video with payload:  %s", event.payload)
        self._handle_update_or_create(event)

    def handle_deleted(self, event: ParsedEvent) -> None:
        """
        Handles the deletion of a video based on the parsed event.

        Args:
            event (ParsedEvent): The event containing the payload for the video to be deleted.
        """

        print("Deleting video:  %s", event.payload)
        # TODO: implement delete use case
