from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from src._shared.listing import ListOutput
from src.application.list_video import ListVideo, ListVideoInput, VideoSortableFields
from src.domain.video import Video
from src.domain.video_repository import VideoRepository
from src.infra.api.http._shared.dependencies import (
    common_query_params,
    get_video_repository,
)

router = APIRouter()


@router.get(
    path="/",
    response_model=ListOutput[Video],
)
def list_categories(
    repository: VideoRepository = Depends(get_video_repository),
    sort: VideoSortableFields = Query(
        default=VideoSortableFields.TITLE,
        description="Field to sort by",
    ),
    query_params: Dict[str, Any] = Depends(common_query_params),
) -> ListOutput[Video]:
    """
    Retrieves a list of categories.

    This endpoint uses the ListVideo use case to retrieve and return
    categories. The categories are fetched from an Elasticsearch repository
    and returned in a structured format defined by ListOutput.

    Returns:
        ListOutput[Video]: A structured list of categories.
    """

    use_case = ListVideo(repository)
    response = use_case.execute(
        ListVideoInput(
            page=query_params["page"],
            per_page=query_params["per_page"],
            sort=sort,
            direction=query_params["direction"],
            search=query_params["search"],
        )
    )
    return response
