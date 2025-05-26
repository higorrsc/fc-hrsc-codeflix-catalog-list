import logging
from typing import List, Optional

from elasticsearch import Elasticsearch
from pydantic import ValidationError

from src._shared.constants import (
    DEFAULT_PAGINATION_SIZE,
    ELASTICSEARCH_CATEGORY_INDEX,
    ELASTICSEARCH_HOST,
)
from src.category import Category
from src.category_repository import CategoryRepository, SortDirection


class ElasticsearchCategoryRepository(CategoryRepository):
    """
    A repository for managing categories in Elasticsearch.
    This class implements the CategoryRepository interface and provides methods
    for searching categories with pagination, sorting, and filtering capabilities.
    """

    def __init__(
        self,
        client: Optional[Elasticsearch] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initializes a new instance of the ElasticsearchCategoryRepository class.

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
    ) -> List[Category]:
        """
        Searches for categories based on the given filters.

        Args:
            page (int): The page to be returned. Defaults to 1.
            per_page (int): The number of items per page. Defaults to 5.
            search (str | None): The search query. Defaults to None.
            sort (str | None): The name of the field to sort by. Defaults to None.
            direction (SortDirection): The sort direction. Defaults to ASC.

        Returns:
            List[Category]: A list of categories.
        """

        response = self._client.search(index=ELASTICSEARCH_CATEGORY_INDEX, body={})
        category_hits = response.get("hits", {}).get("hits", [])
        parsed_categories: List[Category] = []
        for category in category_hits:
            try:
                parsed_category = Category(**category["_source"])
            except ValidationError as e:
                self._logger.error("Error parsing category %s: %s", category["_id"], e)
            else:
                parsed_categories.append(parsed_category)

        return parsed_categories
