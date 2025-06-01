import logging
from unittest.mock import create_autospec
from uuid import uuid4

from elasticsearch import Elasticsearch

from src._shared.constants import ELASTICSEARCH_GENRE_INDEX
from src._shared.listing import SortDirection
from src.application.list_genre import GenreSortableFields
from src.domain.genre import Genre
from src.infra.elasticsearch.elasticsearch_genre_repository import (
    ElasticsearchGenreRepository,
)


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

        repository = ElasticsearchGenreRepository(es)
        result = repository.search()
        assert not result

    def test_when_index_has_genres_then_return_mapped_genres_with_default_search(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When the index has genres, the repository should return a list of mapped
        genres with the default search
        """

        repository = ElasticsearchGenreRepository(populated_es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            drama,
            horror,
        ]

    def test_when_index_has_malformed_genres_then_return_valid_genres_and_log_error(
        self,
        es: Elasticsearch,
        drama: Genre,
    ) -> None:
        """
        When the index has malformed genres, the repository should return
        valid genres and log an error.
        """

        es.index(
            index=ELASTICSEARCH_GENRE_INDEX,
            id=str(drama.id),
            body=drama.model_dump(mode="json"),
            refresh=True,
        )
        es.index(
            index=ELASTICSEARCH_GENRE_INDEX,
            id=str(uuid4()),
            body={"name": "Malformed"},
            refresh=True,
        )
        mock_logger = create_autospec(logging.Logger)
        repository = ElasticsearchGenreRepository(client=es, logger=mock_logger)

        genres = repository.search()

        assert genres == [drama]
        mock_logger.error.assert_called_once()

    def test_when_search_term_matches_genre_name_then_return_matching_entities(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When the search term matches a genre name, the repository should return matching
        genres.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        result = repository.search(search="Drama")
        assert result == [drama]

        result = repository.search(search="Horror")
        assert result == [horror]

        result = repository.search(
            search="Gênero",
            sort=GenreSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [
            drama,
            horror,
        ]


class TestSort:
    """
    Test cases for sorting genres in the ElasticsearchGenreRepository
    """

    def test_when_no_sorting_is_specified_then_return_genres_ordered_by_insertion_order(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When no sorting is specified, the repository should return genres ordered by
        insertion order, which is the default order in which the documents were inserted
        into the index.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            drama,
            horror,
        ]

    def test_return_genres_ordered_by_name_asc(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When sorting by name in ascending order, the repository should return
        a list of genres with the names in ascending alphabetical order.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        result = repository.search(
            sort=GenreSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert len(result) == 2
        assert result == [
            drama,
            horror,
        ]

    def test_return_genres_ordered_by_name_desc(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When sorting by name in descending order, the repository should return
        a list of genres with the names in descending alphabetical order.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        result = repository.search(
            sort=GenreSortableFields.NAME,  # type: ignore
            direction=SortDirection.DESC,
        )
        assert len(result) == 2
        assert result == [
            horror,
            drama,
        ]


class TestPagination:
    """
    Test cases for pagination in the ElasticsearchGenreRepository
    """

    def test_when_no_page_is_requested_then_return_default_paginated_response(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        When no page is requested, the repository should return a default paginated response.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        assert repository.search() == [
            drama,
            horror,
        ]

    def test_when_page_is_requested_then_return_paginated_response(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:
        """
        Test that when a specific page is requested, the repository returns a paginated response.
        """

        repository = ElasticsearchGenreRepository(populated_es)

        result = repository.search(
            page=1,
            per_page=1,
            sort=GenreSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [drama]

        result = repository.search(
            page=2,
            per_page=1,
            sort=GenreSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [horror]

    def test_when_request_page_is_out_of_bounds_then_return_empty_list(
        self,
        populated_es: Elasticsearch,
    ) -> None:
        """
        When the requested page is out of bounds, the repository should return an empty list.
        """

        repository = ElasticsearchGenreRepository(populated_es)
        assert not repository.search(page=2)
