from typing import Optional

from fastapi import Depends, FastAPI, Query

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutput, SortDirection
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.domain.category import Category
from src.domain.category_repository import CategoryRepository
from src.infra.elasticsearch.elasticsearch_category_repository import (
    ElasticsearchCategoryRepository,
)

app = FastAPI()


@app.get("/healthcheck")
def healthcheck():
    """
    Simple healthcheck endpoint that returns a static ok status.

    This endpoint does not do any actual health checking on the service
    or its dependencies. It is intended to be used by load balancers
    or other infrastructure to quickly check the health of the service.

    Returns:
        dict: A dictionary containing a status key with value 200.
    """

    return {"status": 200}


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


@app.get("/categories")
def list_categories(
    repository: CategoryRepository = Depends(get_category_repository),
    search: Optional[str] = Query(
        default=None,
        description="Search term for name or description",
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
    sort: CategorySortableFields = Query(
        default=CategorySortableFields.NAME,
        description="Field to sort by",
    ),
    direction: SortDirection = Query(
        default=SortDirection.ASC,
        description="Sort direction",
    ),
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
            page=page,
            per_page=per_page,
            sort=sort,
            direction=direction,
            search=search,
        )
    )
    return response
