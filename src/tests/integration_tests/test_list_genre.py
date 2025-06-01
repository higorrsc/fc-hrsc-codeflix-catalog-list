from elasticsearch import Elasticsearch

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutput, ListOutputMeta, SortDirection
from src.application.list_genre import GenreSortableFields, ListGenre, ListGenreInput
from src.domain.genre import Genre
from src.infra.elasticsearch.elasticsearch_genre_repository import (
    ElasticsearchGenreRepository,
)


class TestListGenre:
    """
    Test suite for the ListGenre use case.
    """

    def test_list_categories_with_default_values(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
        horror: Genre,
    ) -> None:

        list_genre = ListGenre(ElasticsearchGenreRepository(populated_es))
        output = list_genre.execute(ListGenreInput())

        assert output.data == [
            drama,
            horror,
        ]
        assert output.meta == ListOutputMeta(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=GenreSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output.data) == 2

        assert output == ListOutput(
            data=[
                drama,
                horror,
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=DEFAULT_PAGINATION_SIZE,
                sort=GenreSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

    def test_list_categories_with_pagination_sorting_and_search(
        self,
        populated_es: Elasticsearch,
        drama: Genre,
    ) -> None:
        list_genre = ListGenre(ElasticsearchGenreRepository(populated_es))

        output_page_1 = list_genre.execute(
            ListGenreInput(
                page=1,
                per_page=1,
                sort=GenreSortableFields.NAME,
                direction=SortDirection.ASC,
                search="Drama",
            )
        )

        assert output_page_1.data == [drama]
        assert output_page_1.meta == ListOutputMeta(
            page=1,
            per_page=1,
            sort=GenreSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_1.data) == 1

        assert output_page_1 == ListOutput(
            data=[drama],
            meta=ListOutputMeta(
                page=1,
                per_page=1,
                sort=GenreSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

        output_page_2 = list_genre.execute(
            ListGenreInput(
                page=2,
                per_page=1,
                sort=GenreSortableFields.NAME,
                direction=SortDirection.ASC,
                search="Drama",
            )
        )

        assert output_page_2.data == []
        assert output_page_2.meta == ListOutputMeta(
            page=2,
            per_page=1,
            sort=GenreSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_2.data) == 0

        assert output_page_2 == ListOutput(
            data=[],
            meta=ListOutputMeta(
                page=2,
                per_page=1,
                sort=GenreSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )
