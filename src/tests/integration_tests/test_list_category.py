from datetime import datetime
from uuid import uuid4

import pytest
from elasticsearch import Elasticsearch

from src._shared.constants import DEFAULT_PAGINATION_SIZE, ELASTICSEARCH_CATEGORY_INDEX
from src.application.list_category import (
    ListCategory,
    ListCategoryInput,
    ListCategoryOutput,
    ListCategoryOutputMeta,
    SortableFields,
)
from src.domain.category import Category
from src.domain.category_repository import SortDirection
from src.infra.elasticsearch.elasticsearch_category_repository import (
    ElasticsearchCategoryRepository,
)


@pytest.fixture
def movie_category() -> Category:
    """
    Fixture that returns a Category instance representing a movie category.

    Returns:
        Category: A Category object with predefined attributes for testing.
    """

    return Category(
        id=uuid4(),
        name="Filme",
        description="Categoria de filmes",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def series_category() -> Category:
    """
    Fixture that returns a Category instance representing a series category.

    Returns:
        Category: A Category object with predefined attributes for testing.
    """

    return Category(
        id=uuid4(),
        name="Séries",
        description="Categoria de séries",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def documentary_category() -> Category:
    """
    Fixture that returns a Category instance representing a documentary category.

    Returns:
        Category: A Category object with predefined attributes for testing.
    """

    return Category(
        id=uuid4(),
        name="Documentários",
        description="Categoria de documentários",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def es() -> Elasticsearch:  # type: ignore
    """
    Fixture to create an Elasticsearch client connected to the test instance
    """
    elasticsearch_client = Elasticsearch(hosts=["http://localhost:9201"])
    if not elasticsearch_client.indices.exists(index=ELASTICSEARCH_CATEGORY_INDEX):
        elasticsearch_client.indices.create(index=ELASTICSEARCH_CATEGORY_INDEX)

    yield elasticsearch_client  # type: ignore

    elasticsearch_client.indices.delete(index=ELASTICSEARCH_CATEGORY_INDEX)


@pytest.fixture
def populated_es(
    es: Elasticsearch,  # type: ignore
    movie_category: Category,
    series_category: Category,
    documentary_category: Category,
) -> Elasticsearch:  # type: ignore
    """
    Fixture to create an Elasticsearch client connected to the test instance
    """

    elasticsearch_client = es
    elasticsearch_client.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(movie_category.id),
        body=movie_category.model_dump(mode="json"),
        refresh=True,
    )
    elasticsearch_client.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(series_category.id),
        body=series_category.model_dump(mode="json"),
        refresh=True,
    )
    elasticsearch_client.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(documentary_category.id),
        body=documentary_category.model_dump(mode="json"),
        refresh=True,
    )

    return elasticsearch_client


class TestListCategory:
    """
    Test suite for the ListCategory use case.
    """

    def test_list_categories_with_default_values(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
        documentary_category: Category,
    ) -> None:
        """
        Should return a list of categories with default values.

        When calling ListCategory.execute with default values, it should return a list of
        categories with the default values.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.
            documentary_category (Category): A Category instance representing a documentary category.

        Returns:
            None
        """
        list_category = ListCategory(ElasticsearchCategoryRepository(populated_es))
        output = list_category.execute(ListCategoryInput())

        assert output.data == [
            documentary_category,
            movie_category,
            series_category,
        ]
        assert output.meta == ListCategoryOutputMeta(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output.data) == 3

        assert output == ListCategoryOutput(
            data=[
                documentary_category,
                movie_category,
                series_category,
            ],
            meta=ListCategoryOutputMeta(
                page=1,
                per_page=DEFAULT_PAGINATION_SIZE,
                sort=SortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

    def test_list_categories_with_pagination_sorting_and_search(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
        documentary_category: Category,
    ) -> None:
        list_category = ListCategory(ElasticsearchCategoryRepository(populated_es))

        output_page_1 = list_category.execute(
            ListCategoryInput(
                page=1,
                per_page=1,
                sort=SortableFields.NAME,
                direction=SortDirection.ASC,
                search="Filme",
            )
        )

        assert output_page_1.data == [movie_category]
        assert output_page_1.meta == ListCategoryOutputMeta(
            page=1,
            per_page=1,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_1.data) == 1

        assert output_page_1 == ListCategoryOutput(
            data=[movie_category],
            meta=ListCategoryOutputMeta(
                page=1,
                per_page=1,
                sort=SortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

        output_page_2 = list_category.execute(
            ListCategoryInput(
                page=2,
                per_page=1,
                sort=SortableFields.NAME,
                direction=SortDirection.ASC,
                search="Filme",
            )
        )

        assert output_page_2.data == []
        assert output_page_2.meta == ListCategoryOutputMeta(
            page=2,
            per_page=1,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_2.data) == 0

        assert output_page_2 == ListCategoryOutput(
            data=[],
            meta=ListCategoryOutputMeta(
                page=2,
                per_page=1,
                sort=SortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )
