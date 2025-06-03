import strawberry

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import SortDirection
from src.application.list_cast_member import (
    CastMemberSortableFields,
    ListCastMember,
    ListCastMemberInput,
)
from src.domain.cast_member import CastMember
from src.infra.api._shared.dependencies import get_cast_member_repository
from src.infra.api._shared.graphql import Meta, Result


@strawberry.experimental.pydantic.type(model=CastMember)
class CastMemberGraphQL:
    """
    CastMember GraphQL type
    """

    id: strawberry.auto
    name: strawberry.auto
    type: strawberry.auto


def get_cast_members(
    sort: CastMemberSortableFields = CastMemberSortableFields.NAME,
    search: str | None = None,
    page: int = 1,
    per_page: int = DEFAULT_PAGINATION_SIZE,
    direction: SortDirection = SortDirection.ASC,
) -> Result[CastMemberGraphQL]:
    """
    Retrieves a list of categories

    This resolver uses the ListCastMember use case to retrieve and return
    categories. The categories are fetched from an Elasticsearch repository
    and returned in a structured format defined by Result.

    Returns:
        Result[CastMemberGraphQL]: A structured list of categories.
    """

    repository = get_cast_member_repository()
    use_case = ListCastMember(repository=repository)
    output = use_case.execute(
        ListCastMemberInput(
            search=search,
            page=page,
            per_page=per_page,
            sort=sort,
            direction=direction,
        )
    )

    return Result(
        data=[CastMemberGraphQL.from_pydantic(category) for category in output.data],
        meta=Meta.from_pydantic(output.meta),  # type: ignore
    )
