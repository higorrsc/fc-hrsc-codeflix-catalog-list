from elasticsearch import Elasticsearch

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutput, ListOutputMeta, SortDirection
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.domain.category import Category
from src.infra.elasticsearch.elasticsearch_category_repository import (
    ElasticsearchCategoryRepository,
)


class TestListCategory:
    """
    Test suite for the ListCategory use case.
    """

    def test_list_categories_with_default_values(
        self,
        populated_es: Elasticsearch,
        movie: Category,
        series: Category,
        documentary: Category,
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
            documentary,
            movie,
            series,
        ]
        assert output.meta == ListOutputMeta(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output.data) == 3

        assert output == ListOutput(
            data=[
                documentary,
                movie,
                series,
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=DEFAULT_PAGINATION_SIZE,
                sort=CategorySortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

    def test_list_categories_with_pagination_sorting_and_search(
        self,
        populated_es: Elasticsearch,
        movie: Category,
        series: Category,
        documentary: Category,
    ) -> None:
        list_category = ListCategory(ElasticsearchCategoryRepository(populated_es))

        output_page_1 = list_category.execute(
            ListCategoryInput(
                page=1,
                per_page=1,
                sort=CategorySortableFields.NAME,
                direction=SortDirection.ASC,
                search="Filme",
            )
        )

        assert output_page_1.data == [movie]
        assert output_page_1.meta == ListOutputMeta(
            page=1,
            per_page=1,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_1.data) == 1

        assert output_page_1 == ListOutput(
            data=[movie],
            meta=ListOutputMeta(
                page=1,
                per_page=1,
                sort=CategorySortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

        output_page_2 = list_category.execute(
            ListCategoryInput(
                page=2,
                per_page=1,
                sort=CategorySortableFields.NAME,
                direction=SortDirection.ASC,
                search="Filme",
            )
        )

        assert output_page_2.data == []
        assert output_page_2.meta == ListOutputMeta(
            page=2,
            per_page=1,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_2.data) == 0

        assert output_page_2 == ListOutput(
            data=[],
            meta=ListOutputMeta(
                page=2,
                per_page=1,
                sort=CategorySortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )
