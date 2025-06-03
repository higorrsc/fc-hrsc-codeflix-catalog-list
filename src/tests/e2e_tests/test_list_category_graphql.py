from typing import Iterator
from unittest.mock import MagicMock, patch

import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient

from src.domain.category import Category
from src.domain.category_repository import CategoryRepository
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


@patch("src.infra.api.graphql.schema.schema.get_category_repository")
def test_list_categories(
    mock_category_repository: MagicMock,
    populated_category_repository: CategoryRepository,
    series: Category,
    movie: Category,
    documentary: Category,
) -> None:
    mock_category_repository.return_value = populated_category_repository
    query = """
    {
        categories {
            data {
                id,
                name,
                description
            },
            meta {
                page,
                per_page,
                sort,
                direction                
            }
        }
    }
    """

    client = TestClient(app)
    response = client.post(url="/graphql", json={"query": query})
    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "categories": {
                "data": [
                    {
                        "id": str(documentary.id),
                        "name": documentary.name,
                        "description": documentary.description,
                    },
                    {
                        "id": str(movie.id),
                        "name": movie.name,
                        "description": movie.description,
                    },
                    {
                        "id": str(series.id),
                        "name": series.name,
                        "description": series.description,
                    },
                ],
                "meta": {
                    "page": 1,
                    "per_page": 5,
                    "sort": "name",
                    "direction": "ASC",
                },
            }
        }
    }
