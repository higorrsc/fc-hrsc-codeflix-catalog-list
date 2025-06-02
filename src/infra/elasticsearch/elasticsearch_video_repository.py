import logging
from typing import List, Optional

from elasticsearch import Elasticsearch, NotFoundError
from pydantic import ValidationError

from src._shared.constants import (
    DEFAULT_PAGINATION_SIZE,
    ELASTICSEARCH_HOST,
    ELASTICSEARCH_VIDEO_INDEX,
)
from src._shared.listing import SortDirection
from src.application.list_video import VideoSortableFields
from src.domain.video import Video
from src.domain.video_repository import VideoRepository


class ElasticsearchVideoRepository(VideoRepository):
    """
    A repository for managing categories in Elasticsearch.
    This class implements the VideoRepository interface and provides methods
    for searching categories with pagination, sorting, and filtering capabilities.
    """

    def __init__(
        self,
        client: Optional[Elasticsearch] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initializes a new instance of the ElasticsearchVideoRepository class.

        Args:
            client (Optional[Elasticsearch]): The Elasticsearch client to use. If None, a
                new client will be created with the default host.
            logger (Optional[logging.Logger]): The logger to use for logging within this
                repository. If None, a default logger will be created.
        """

        self._client = client or Elasticsearch(hosts=[ELASTICSEARCH_HOST])
        self._logger = logger or logging.getLogger(__name__)

    def search(  # type: ignore
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: Optional[str] = None,
        sort: Optional[VideoSortableFields] = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> List[Video]:
        """
        Searches for videos based on the given filters.

        Args:
            page (int): The page to be returned. Defaults to 1.
            per_page (int): The number of items per page. Defaults to 5.
            search (str | None): The search query. Defaults to None.
            sort (str | None): The name of the field to sort by. Defaults to None.
            direction (SortDirection): The sort direction. Defaults to ASC.

        Returns:
            List[Video]: A list of videos.
        """

        try:
            response = self._client.search(
                index=ELASTICSEARCH_VIDEO_INDEX,
                body={
                    "sort": [{f"{sort}.keyword": {"order": direction}}] if sort else [],
                    "from": (page - 1) * per_page,
                    "size": per_page,
                    "query": {
                        "bool": {
                            "must": (
                                [
                                    {
                                        "multi_match": {
                                            "query": search,
                                            "fields": ["title"],
                                        }
                                    }
                                ]
                                if search
                                else [{"match_all": {}}]
                            )
                        }
                    },
                },
            )
            video_hits = response["hits"]["hits"]
        except NotFoundError:
            self._logger.error("Index %s not found", ELASTICSEARCH_VIDEO_INDEX)
            return []

        parsed_entities = []
        for hit in video_hits:
            try:
                parsed_entity = Video(**hit["_source"])
            except ValidationError:
                self._logger.error(f"Malformed entity: {hit}")
            else:
                parsed_entities.append(parsed_entity)

        return parsed_entities

    def save(self, video: Video) -> None:
        """
        Saves a video to the Elasticsearch index.

        Args:
            video (Video): The video object to be indexed in Elasticsearch.

        Raises:
            ValidationError: If the video object is not valid.
        """

        self._client.index(
            index=ELASTICSEARCH_VIDEO_INDEX,
            id=str(video.id),
            body=video.model_dump(mode="json"),
        )
