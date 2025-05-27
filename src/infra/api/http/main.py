from fastapi import Depends, FastAPI

from src._shared.listing import ListOutput
from src.application.list_category import ListCategory, ListCategoryInput
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
    response = use_case.execute(ListCategoryInput())
    return response
