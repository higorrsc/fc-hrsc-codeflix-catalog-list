from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from src._shared.listing import ListOutput
from src.application.list_cast_member import (
    CastMemberSortableFields,
    ListCastMember,
    ListCastMemberInput,
)
from src.domain.cast_member import CastMember
from src.domain.cast_member_repository import CastMemberRepository
from src.infra.api._shared.dependencies import (
    common_query_params,
    get_cast_member_repository,
)

router = APIRouter()


@router.get(
    path="/",
    response_model=ListOutput[CastMember],
)
def list_cast_members(
    repository: CastMemberRepository = Depends(get_cast_member_repository),
    sort: CastMemberSortableFields = Query(
        default=CastMemberSortableFields.NAME,
        description="Field to sort by",
    ),
    query_params: Dict[str, Any] = Depends(common_query_params),
) -> ListOutput[CastMember]:
    """
    Retrieves a list of cast members.

    This endpoint uses the ListCastMember use case to retrieve and return
    cast members. The cast members are fetched from an Elasticsearch repository
    and returned in a structured format defined by ListOutput.

    Returns:
        ListOutput[CastMember]: A structured list of cast members.
    """

    use_case = ListCastMember(repository)
    response = use_case.execute(
        ListCastMemberInput(
            **query_params,
            sort=sort,
        )
    )
    return response
