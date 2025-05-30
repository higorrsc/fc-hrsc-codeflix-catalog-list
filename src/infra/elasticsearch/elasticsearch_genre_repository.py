import logging
from typing import List, Optional

from elasticsearch import Elasticsearch
from pydantic import ValidationError

from src._shared.constants import (
    DEFAULT_PAGINATION_SIZE,
    ELASTICSEARCH_GENRE_INDEX,
    ELASTICSEARCH_HOST,
)
from src._shared.listing import SortDirection
from src.domain.genre import Genre
from src.domain.genre_repository import GenreRepository


class ElasticsearchGenreRepository(GenreRepository):
    """
    A repository for managing genres in Elasticsearch.
    This class implements the GenreRepository interface and provides methods
    for searching genres with pagination, sorting, and filtering capabilities.
    """

    def __init__(
        self,
        client: Optional[Elasticsearch] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initializes a new instance of the ElasticsearchGenreRepository class.

        Args:
            client (Optional[Elasticsearch]): The Elasticsearch client to use. If None, a
                new client will be created with the default host.
            logger (Optional[logging.Logger]): The logger to use for logging within this
                repository. If None, a default logger will be created.
        """

        self._client = client or Elasticsearch(hosts=[ELASTICSEARCH_HOST])
        self._logger = logger or logging.getLogger(__name__)

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> List[Genre]:
        """
        Searches for genres based on the given filters.

        Args:
            page (int): The page to be returned. Defaults to 1.
            per_page (int): The number of items per page. Defaults to the default pagination size.
            search (str | None): The search query for cast member fields. Defaults to None.
            sort (str | None): The name of the field to sort by. Defaults to None.
            direction (SortDirection): The sort direction. Defaults to ascending order.

        Returns:
            List[Genre]: A list of genres matching the search criteria.
        """

        response = self._client.search(
            index=ELASTICSEARCH_GENRE_INDEX,
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
                                        "fields": ["name"],
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
        genre_hits = response.get("hits", {}).get("hits", [])
        parsed_genres: List[Genre] = []
        for genre in genre_hits:
            try:
                parsed_genre = Genre(**genre["_source"], categories=set())
            except ValidationError as e:
                self._logger.error("Error parsing genres %s: %s", genre["_id"], e)
            else:
                parsed_genres.append(parsed_genre)

        return parsed_genres
