from unittest.mock import create_autospec

import pytest

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutputMeta, SortDirection
from src.application.list_category import (
    CategorySortableFields,
    ListCategory,
    ListCategoryInput,
)
from src.domain.category import Category
from src.domain.category_repository import CategoryRepository


class TestListCategory:
    """
    Test suite for the ListCategory use case.
    """

    def test_list_categories_with_default_values(
        self,
        movie: Category,
        series: Category,
    ) -> None:
        """
        Should return a list of categories with default values.

        When calling ListCategory.execute with default values, it should return a list of
        categories with the default values.

        Args:
            movie (Category): A Category instance representing a movie category.
            series (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie,
            series,
        ]

        list_category = ListCategory(repository)
        output = list_category.execute(params=ListCategoryInput())

        assert output.data == [
            movie,
            series,
        ]

        assert output.meta == ListOutputMeta(
            page=1,
            per_page=5,
            sort="name",
            direction="asc",  # type: ignore
        )

        repository.search.assert_called_once_with(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=CategorySortableFields.NAME,
            direction=SortDirection.ASC,
            search=None,
        )

    def test_list_categories_with_custom_values(
        self,
        movie: Category,
        series: Category,
    ) -> None:
        """
        Should return a list of categories with custom values.

        When calling ListCategory.execute with custom values, it should return a list of
        categories with the custom values.

        Args:
            movie (Category): A Category instance representing a movie category.
            series (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie,
            series,
        ]

        list_category = ListCategory(repository)
        output = list_category.execute(
            params=ListCategoryInput(
                page=2,
                per_page=10,
                sort=CategorySortableFields.DESCRIPTION,
                direction=SortDirection.DESC,
                search="test",
            )
        )

        assert output.data == [
            movie,
            series,
        ]

        assert output.meta == ListOutputMeta(
            page=2,
            per_page=10,
            sort="description",
            direction="desc",  # type: ignore
        )

        repository.search.assert_called_once_with(
            page=2,
            per_page=10,
            sort=CategorySortableFields.DESCRIPTION,
            direction=SortDirection.DESC,
            search="test",
        )

    def test_list_categories_return_error_with_invalid_sort(
        self,
        movie: Category,
        series: Category,
    ) -> None:
        """
        Should raise an error when an invalid sort field is provided.

        When calling ListCategory.execute with an invalid sort field, it should raise a ValueError.

        Args:
            movie (Category): A Category instance representing a movie category.
            series (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie,
            series,
        ]

        list_category = ListCategory(repository)

        with pytest.raises(ValueError):
            list_category.execute(
                params=ListCategoryInput(
                    sort="invalid_field",  # type: ignore
                )
            )
