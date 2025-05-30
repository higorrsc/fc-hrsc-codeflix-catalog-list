from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from src._shared.listing import ListOutput
from src.application.list_genre import GenreSortableFields, ListGenre, ListGenreInput
from src.domain.genre import Genre
from src.domain.genre_repository import GenreRepository
from src.infra.api.http._shared.dependencies import (
    common_query_params,
    get_genre_repository,
)

router = APIRouter()


@router.get(
    path="/",
    response_model=ListOutput[Genre],
)
def list_genres(
    repository: GenreRepository = Depends(get_genre_repository),
    sort: GenreSortableFields = Query(
        default=GenreSortableFields.NAME,
        description="Field to sort by",
    ),
    query_params: Dict[str, Any] = Depends(common_query_params),
) -> ListOutput[Genre]:
    """
    Retrieves a list of cast members.

    This endpoint uses the ListGenre use case to retrieve and return
    cast members. The cast members are fetched from an Elasticsearch repository
    and returned in a structured format defined by ListOutput.

    Returns:
        ListOutput[Genre]: A structured list of cast members.
    """

    use_case = ListGenre(repository)
    response = use_case.execute(
        ListGenreInput(
            page=query_params["page"],
            per_page=query_params["per_page"],
            sort=sort,
            direction=query_params["direction"],
            search=query_params["search"],
        )
    )
    return response
