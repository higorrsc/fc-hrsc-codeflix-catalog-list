import logging
from datetime import datetime
from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from elasticsearch import Elasticsearch

from src._shared.constants import ELASTICSEARCH_CATEGORY_INDEX
from src.category import Category
from src.elasticsearch_category_repository import ElasticsearchCategoryRepository


class TestSearch:
    """
    Test cases for the Search class that interacts with an Elasticsearch index
    """

    @pytest.fixture
    def es(self) -> Elasticsearch:  # type: ignore
        """
        Fixture to create an Elasticsearch client connected to the test instance
        """
        es = Elasticsearch(hosts=["http://localhost:9201"])
        if not es.indices.exists(index=ELASTICSEARCH_CATEGORY_INDEX):
            es.indices.create(index=ELASTICSEARCH_CATEGORY_INDEX)

        yield es  # type: ignore

        es.indices.delete(index=ELASTICSEARCH_CATEGORY_INDEX)

    @pytest.fixture
    def movie_category(self) -> Category:
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
    def series_category(self) -> Category:
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

    def test_can_reach_test_elasticsearch(self, es: Elasticsearch) -> None:
        """
        Tests that we can connect to the test Elasticsearch instance
        """

        assert es.ping()

    def test_when_index_is_empty_then_return_empty_list(
        self, es: Elasticsearch
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
        When the index has categories, the repository should return a list of mapped categories with the default search
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
