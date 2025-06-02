import logging
from typing import List, Optional

from elasticsearch import Elasticsearch
from pydantic import ValidationError

from src._shared.constants import (
    DEFAULT_PAGINATION_SIZE,
    ELASTICSEARCH_CAST_MEMBER_INDEX,
    ELASTICSEARCH_HOST,
)
from src._shared.listing import SortDirection
from src.application.list_cast_member import CastMemberSortableFields
from src.domain.cast_member import CastMember
from src.domain.cast_member_repository import CastMemberRepository


class ElasticsearchCastMemberRepository(CastMemberRepository):
    """
    A repository for managing cast members in Elasticsearch.
    This class implements the CastMemberRepository interface and provides methods
    for searching cast members with pagination, sorting, and filtering capabilities.
    """

    def __init__(
        self,
        client: Optional[Elasticsearch] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        """
        Initializes a new instance of the ElasticsearchCastMemberRepository class.

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
        sort: Optional[CastMemberSortableFields] = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> List[CastMember]:
        """
        Searches for cast members based on the given filters.

        Args:
            page (int): The page to be returned. Defaults to 1.
            per_page (int): The number of items per page. Defaults to the default pagination size.
            search (str | None): The search query for cast member fields. Defaults to None.
            sort (str | None): The name of the field to sort by. Defaults to None.
            direction (SortDirection): The sort direction. Defaults to ascending order.

        Returns:
            List[CastMember]: A list of cast members matching the search criteria.
        """

        response = self._client.search(
            index=ELASTICSEARCH_CAST_MEMBER_INDEX,
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
                                        "fields": ["name", "type"],
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
        cast_member_hits = response.get("hits", {}).get("hits", [])
        parsed_cast_members: List[CastMember] = []
        for cast_member in cast_member_hits:
            try:
                parsed_cast_member = CastMember(**cast_member["_source"])
            except ValidationError as e:
                self._logger.error(
                    "Error parsing cast members %s: %s", cast_member["_id"], e
                )
            else:
                parsed_cast_members.append(parsed_cast_member)

        return parsed_cast_members
