from typing import Any, Dict

from fastapi import APIRouter, Depends, Query

from src._shared.listing import ListOutput
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.domain.category import Category
from src.domain.category_repository import CategoryRepository
from src.infra.api.http._shared.dependencies import (
    common_query_params,
    get_category_repository,
)

router = APIRouter()


@router.get(
    path="/",
    response_model=ListOutput[Category],
)
def list_categories(
    repository: CategoryRepository = Depends(get_category_repository),
    sort: CategorySortableFields = Query(
        default=CategorySortableFields.NAME,
        description="Field to sort by",
    ),
    query_params: Dict[str, Any] = Depends(common_query_params),
) -> ListOutput[Category]:
    """
    Retrieves a list of categories.

    This endpoint uses the ListCategory use case to retrieve and return
    categories. The categories are fetched from an Elasticsearch repository
    and returned in a structured format defined by ListOutput.

    Returns:
        ListOutput[Category]: A structured list of categories.
    """

    use_case = ListCategory(repository)
    response = use_case.execute(
        ListCategoryInput(
            **query_params,
            sort=sort,
        )
    )
    return response
