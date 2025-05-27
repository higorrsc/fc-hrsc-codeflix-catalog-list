import logging
from datetime import datetime
from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from elasticsearch import Elasticsearch

from src._shared.constants import ELASTICSEARCH_CATEGORY_INDEX
from src._shared.listing import SortDirection
from src.application.list_category import CategorySortableFields
from src.domain.category import Category
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
    movie_category: Category,
    series_category: Category,
) -> Elasticsearch:  # type: ignore
    """
    Fixture to create an Elasticsearch client connected to the test instance
    """
    elasticsearch_client = Elasticsearch(hosts=["http://localhost:9201"])
    if not elasticsearch_client.indices.exists(index=ELASTICSEARCH_CATEGORY_INDEX):
        elasticsearch_client.indices.create(index=ELASTICSEARCH_CATEGORY_INDEX)

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

    yield elasticsearch_client  # type: ignore

    elasticsearch_client.indices.delete(index=ELASTICSEARCH_CATEGORY_INDEX)


class TestSearch:
    """
    Test cases for the Search class that interacts with an Elasticsearch index
    """

    def test_can_reach_test_elasticsearch(
        self,
        es: Elasticsearch,
    ) -> None:
        """
        Tests that we can connect to the test Elasticsearch instance
        """

        assert es.ping()

    def test_when_index_is_empty_then_return_empty_list(
        self,
        es: Elasticsearch,
    ) -> None:
        """
        When the index is empty, the repository should return an empty list.
        """

        repository = ElasticsearchCategoryRepository(es)
        result = repository.search()
        assert not result

    def test_when_index_has_categories_then_return_mapped_categories_with_default_search(
        self,
        es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        When the index has categories, the repository should return a list of mapped
        categories with the default search
        """

        es.index(
            index=ELASTICSEARCH_CATEGORY_INDEX,
            id=str(movie_category.id),
            body=movie_category.model_dump(mode="json"),
            refresh=True,
        )
        es.index(
            index=ELASTICSEARCH_CATEGORY_INDEX,
            id=str(series_category.id),
            body=series_category.model_dump(mode="json"),
            refresh=True,
        )

        repository = ElasticsearchCategoryRepository(es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            movie_category,
            series_category,
        ]

    def test_when_index_has_malformed_categories_then_return_valid_categories_and_log_error(
        self,
        es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        When the index has malformed categories, the repository should return
        valid categories and log an error.
        """

        movie_category.id = "malformed_id"  # type: ignore
        es.index(
            index=ELASTICSEARCH_CATEGORY_INDEX,
            id=str(movie_category.id),
            body=movie_category.model_dump(mode="json"),
            refresh=True,
        )
        es.index(
            index=ELASTICSEARCH_CATEGORY_INDEX,
            id=str(series_category.id),
            body=series_category.model_dump(mode="json"),
            refresh=True,
        )

        mock_logger = create_autospec(logging.Logger)
        repository = ElasticsearchCategoryRepository(es, mock_logger)

        assert repository.search() == [series_category]
        mock_logger.error.assert_called_once()

    def test_when_search_term_matches_category_name_then_return_matching_entities(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        When the search term matches a category name, the repository should return matching
        categories.

        This test adds two categories to the Elasticsearch index, and verifies that the
        ElasticsearchCategoryRepository returns the correct categories when searching for a
        term that matches a category name.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = ElasticsearchCategoryRepository(populated_es)
        result = repository.search(search="Filme")
        assert result == [movie_category]

        result = repository.search(search="Séries")
        assert result == [series_category]

        result = repository.search(
            search="Categoria",
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert result == [
            movie_category,
            series_category,
        ]


class TestSort:
    """
    Test cases for sorting categories in the ElasticsearchCategoryRepository
    """

    def test_when_no_sorting_is_specified_then_return_categories_ordered_by_insertion_order(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Test that when no sorting is specified, categories are returned in insertion order.

        This test adds two categories to the Elasticsearch index without specifying any sorting
        parameters, and verifies that the ElasticsearchCategoryRepository returns the categories
        in the order they were inserted.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = ElasticsearchCategoryRepository(populated_es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            movie_category,
            series_category,
        ]

    def test_return_categories_ordered_by_name_asc(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Test that when sorting by name in ascending order, categories are returned in the correct
        order.

        This test adds two categories to the Elasticsearch index, one with a name that comes
        first in a lexicographical sort and one that comes second, and verifies that the
        ElasticsearchCategoryRepository returns the categories in the correct order when
        sorting by name in ascending order.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """
        repository = ElasticsearchCategoryRepository(populated_es)
        result = repository.search(
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(result) == 2
        assert result == [
            movie_category,
            series_category,
        ]

    def test_return_categories_ordered_by_name_desc(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Test that when sorting by name in descending order, categories are returned in the correct
        order.

        This test adds two categories to the Elasticsearch index, one with a name that comes
        second in a lexicographical sort and one that comes first, and verifies that the
        ElasticsearchCategoryRepository returns the categories in the correct order when
        sorting by name in descending order.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = ElasticsearchCategoryRepository(populated_es)
        result = repository.search(
            sort=CategorySortableFields.NAME,
            direction=SortDirection.DESC,
        )
        assert len(result) == 2
        assert result == [
            series_category,
            movie_category,
        ]


class TestPagination:
    """
    Test cases for pagination in the ElasticsearchCategoryRepository
    """

    def test_when_no_page_is_requested_then_return_default_paginated_response(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        When no page is requested, the repository should return a default paginated response.

        When calling the search method of the ElasticsearchCategoryRepository without
        specifying a page, it should return a list of categories with the default pagination
        values.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """
        repository = ElasticsearchCategoryRepository(populated_es)
        assert repository.search() == [
            movie_category,
            series_category,
        ]

    def test_when_page_is_requested_then_return_paginated_response(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Test that when a specific page is requested, the repository returns a paginated response.

        This test ensures that when requesting a specific page with a specified number of items
        per page, the ElasticsearchCategoryRepository returns the correct subset of categories
        that belong to that page.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                        instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = ElasticsearchCategoryRepository(populated_es)

        result = repository.search(
            page=1,
            per_page=1,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert result == [movie_category]

        result = repository.search(
            page=2,
            per_page=1,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert result == [series_category]

    def test_when_request_page_is_out_of_bounds_then_return_empty_list(
        self,
        populated_es: Elasticsearch,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Test that when a page number is requested that is out of bounds, an empty list is returned.

        This test ensures that when requesting a page that is out of bounds, the
        ElasticsearchCategoryRepository returns an empty list.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                        instance.
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = ElasticsearchCategoryRepository(populated_es)
        assert not repository.search(page=2)
