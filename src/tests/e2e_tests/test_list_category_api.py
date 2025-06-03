from typing import Iterator

import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient

from src.domain.category import Category
from src.domain.category_repository import CategoryRepository
from src.infra.api._shared.dependencies import get_category_repository
from src.infra.api.http.main import app
from src.infra.elasticsearch.elasticsearch_category_repository import (
    ElasticsearchCategoryRepository,
)


@pytest.fixture
def populated_category_repository(
    populated_es: Elasticsearch,
) -> Iterator[CategoryRepository]:
    """
    Fixture to provide a CategoryRepository instance populated with test data.

    This fixture creates a CategoryRepository instance backed by an Elasticsearch
    client that has been pre-populated with test categories. It is used to inject
    a repository with data for testing purposes.

    Args:
        populated_es (Elasticsearch): The Elasticsearch client fixture pre-populated
                                      with test categories.

    Yields:
        Iterator[CategoryRepository]: A repository instance with pre-populated categories.
    """

    yield ElasticsearchCategoryRepository(client=populated_es)


@pytest.fixture
def test_client_with_populated_repo(
    populated_category_repository: CategoryRepository,
) -> Iterator[TestClient]:
    """
    Fixture to provide a FastAPI TestClient instance with a populated CategoryRepository.

    This fixture creates a TestClient instance that is configured to use the
    populated_category_repository fixture for the ListCategory use case. It is
    used to test the ListCategory API endpoint with pre-populated categories.

    Args:
        populated_category_repository (CategoryRepository): A CategoryRepository
            instance pre-populated with test categories.

    Yields:
        Iterator[TestClient]: A TestClient instance with a populated repository.
    """

    app.dependency_overrides[get_category_repository] = (
        lambda: populated_category_repository
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_categories(
    test_client_with_populated_repo: TestClient,
    series: Category,
    movie: Category,
    documentary: Category,
) -> None:
    """
    Should return a list of categories with default pagination values.

    When calling the "/categories" endpoint, it should return a list of categories
    with the default pagination values. The test uses a TestClient instance with
    a populated CategoryRepository instance to test the ListCategory API
    endpoint.

    Args:
        test_client_with_populated_repo (TestClient): A TestClient instance with
            a populated CategoryRepository instance.
        series (Category): A Category instance representing a series category.
        movie (Category): A Category instance representing a movie category.
        documentary (Category): A Category instance representing a documentary
            category.

    Returns:
        None
    """

    response = test_client_with_populated_repo.get("/categories")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": str(documentary.id),
                "name": documentary.name,
                "description": documentary.description,
                "created_at": documentary.created_at.isoformat(),
                "updated_at": documentary.updated_at.isoformat(),
                "is_active": documentary.is_active,
            },
            {
                "id": str(movie.id),
                "name": movie.name,
                "description": movie.description,
                "created_at": movie.created_at.isoformat(),
                "updated_at": movie.updated_at.isoformat(),
                "is_active": movie.is_active,
            },
            {
                "id": str(series.id),
                "name": series.name,
                "description": series.description,
                "created_at": series.created_at.isoformat(),
                "updated_at": series.updated_at.isoformat(),
                "is_active": series.is_active,
            },
        ],
        "meta": {
            "page": 1,
            "per_page": 5,
            "sort": "name",
            "direction": "asc",
        },
    }
