from typing import Any, Dict, Optional

from fastapi import Query

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import SortDirection
from src.infra.elasticsearch.elasticsearch_cast_member_repository import (
    ElasticsearchCastMemberRepository,
)
from src.infra.elasticsearch.elasticsearch_category_repository import (
    ElasticsearchCategoryRepository,
)
from src.infra.elasticsearch.elasticsearch_genre_repository import (
    ElasticsearchGenreRepository,
)
from src.infra.elasticsearch.elasticsearch_video_repository import (
    ElasticsearchVideoRepository,
)


def common_query_params(
    search: Optional[str] = Query(
        default=None,
        description="Search term for text fields",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number",
    ),
    per_page: int = Query(
        default=DEFAULT_PAGINATION_SIZE,
        ge=1,
        le=100,
        description="Number of items per page",
    ),
    direction: SortDirection = Query(
        default=SortDirection.ASC,
        description="Sort direction",
    ),
) -> Dict[str, Any]:
    """
    Common query parameters for pagination and search.

    Args:
        search (str | None): The search query to filter text fields.
        page (int): The page number. Defaults to 1.
        per_page (int): The number of items per page. Defaults to DEFAULT_PAGINATION_SIZE.
        direction (SortDirection): The sort direction. Defaults to SortDirection.ASC.

    Returns:
        A dictionary with the following keys:
            - search
            - page
            - per_page
            - direction
    """

    return {
        "search": search,
        "page": page,
        "per_page": per_page,
        "direction": direction,
    }


def get_category_repository() -> ElasticsearchCategoryRepository:
    """
    Returns a new instance of the ElasticsearchCategoryRepository class.

    This function is used by the app to create a new instance of the
    ElasticsearchCategoryRepository class. It is intended to be used
    as a dependency injection point for the ListCategory use case.

    Returns:
        ElasticsearchCategoryRepository: A new instance of the
            ElasticsearchCategoryRepository class.
    """

    return ElasticsearchCategoryRepository()


def get_cast_member_repository() -> ElasticsearchCastMemberRepository:
    """
    Returns a new instance of the ElasticsearchCastMemberRepository class.

    This function is used by the app to create a new instance of the
    ElasticsearchCastMemberRepository class. It is intended to be used
    as a dependency injection point for the ListCastMember use case.

    Returns:
        ElasticsearchCastMemberRepository: A new instance of the
            ElasticsearchCastMemberRepository class.
    """

    return ElasticsearchCastMemberRepository()


def get_genre_repository() -> ElasticsearchGenreRepository:
    """
    Returns a new instance of the ElasticsearchGenreRepository class.

    This function is used by the app to create a new instance of the
    ElasticsearchGenreRepository class. It is intended to be used
    as a dependency injection point for the ListGenre use case.

    Returns:
        ElasticsearchGenreRepository: A new instance of the
            ElasticsearchGenreRepository class.
    """

    return ElasticsearchGenreRepository()


def get_video_repository() -> ElasticsearchVideoRepository:
    """
    Returns a new instance of the ElasticsearchVideoRepository class.

    This function is used by the app to create a new instance of the
    ElasticsearchVideoRepository class. It is intended to be used
    as a dependency injection point for the ListVideo use case.

    Returns:
        ElasticsearchVideoRepository: A new instance of the
            ElasticsearchVideoRepository class.
    """

    return ElasticsearchVideoRepository()
