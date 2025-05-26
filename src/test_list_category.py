from datetime import datetime
from unittest.mock import create_autospec
from uuid import uuid4

import pytest

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src.category import Category
from src.category_repository import CategoryRepository, SortDirection
from src.list_category import (
    ListCategory,
    ListCategoryInput,
    ListCategoryOutputMeta,
    SortableFields,
)


class TestListCategory:
    """
    Test suite for the ListCategory use case.
    """

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

    def test_list_categories_with_default_values(
        self,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Should return a list of categories with default values.

        When calling ListCategory.execute with default values, it should return a list of
        categories with the default values.

        Args:
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie_category,
            series_category,
        ]

        list_category = ListCategory(repository)
        output = list_category.execute(params=ListCategoryInput())

        assert output.data == [
            movie_category,
            series_category,
        ]

        assert output.meta == ListCategoryOutputMeta(
            page=1,
            per_page=5,
            sort="name",
            direction="asc",  # type: ignore
        )

        repository.search.assert_called_once_with(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
            search=None,
        )

    def test_list_categories_with_custom_values(
        self,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Should return a list of categories with custom values.

        When calling ListCategory.execute with custom values, it should return a list of
        categories with the custom values.

        Args:
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie_category,
            series_category,
        ]

        list_category = ListCategory(repository)
        output = list_category.execute(
            params=ListCategoryInput(
                page=2,
                per_page=10,
                sort=SortableFields.DESCRIPTION,
                direction=SortDirection.DESC,
                search="test",
            )
        )

        assert output.data == [
            movie_category,
            series_category,
        ]

        assert output.meta == ListCategoryOutputMeta(
            page=2,
            per_page=10,
            sort="description",
            direction="desc",  # type: ignore
        )

        repository.search.assert_called_once_with(
            page=2,
            per_page=10,
            sort=SortableFields.DESCRIPTION,
            direction=SortDirection.DESC,
            search="test",
        )

    def test_list_categories_return_error_with_invalid_sort(
        self,
        movie_category: Category,
        series_category: Category,
    ) -> None:
        """
        Should raise an error when an invalid sort field is provided.

        When calling ListCategory.execute with an invalid sort field, it should raise a ValueError.

        Args:
            movie_category (Category): A Category instance representing a movie category.
            series_category (Category): A Category instance representing a series category.

        Returns:
            None
        """

        repository = create_autospec(CategoryRepository)
        repository.search.return_value = [
            movie_category,
            series_category,
        ]

        list_category = ListCategory(repository)

        with pytest.raises(ValueError):
            list_category.execute(
                params=ListCategoryInput(
                    sort="invalid_field",
                )
            )
