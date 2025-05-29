from unittest.mock import create_autospec

import pytest

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutputMeta, SortDirection
from src.application.list_cast_member import (
    CastMemberSortableFields,
    ListCastMember,
    ListCastMemberInput,
)
from src.domain.cast_member import CastMember
from src.domain.cast_member_repository import CastMemberRepository


class TestListCastMember:
    """
    Test suite for the ListCastMember use case.
    """

    def test_list_categories_with_default_values(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Should return a list of categories with default values.

        When calling ListCastMember.execute with default values, it should return a list of
        categories with the default values.

        Args:
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = create_autospec(CastMemberRepository)
        repository.search.return_value = [
            actor,
            director,
        ]

        list_cast_member = ListCastMember(repository)
        output = list_cast_member.execute(params=ListCastMemberInput())

        assert output.data == [
            actor,
            director,
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
            sort=CastMemberSortableFields.NAME,
            direction=SortDirection.ASC,
            search=None,
        )

    def test_list_categories_with_custom_values(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Should return a list of categories with custom values.

        When calling ListCastMember.execute with custom values, it should return a list of
        categories with the custom values.

        Args:
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = create_autospec(CastMemberRepository)
        repository.search.return_value = [
            actor,
            director,
        ]

        list_cast_member = ListCastMember(repository)
        output = list_cast_member.execute(
            params=ListCastMemberInput(
                page=2,
                per_page=10,
                sort=CastMemberSortableFields.TYPE,
                direction=SortDirection.DESC,
                search="test",
            )
        )

        assert output.data == [
            actor,
            director,
        ]

        assert output.meta == ListOutputMeta(
            page=2,
            per_page=10,
            sort="type",
            direction="desc",  # type: ignore
        )

        repository.search.assert_called_once_with(
            page=2,
            per_page=10,
            sort=CastMemberSortableFields.TYPE,
            direction=SortDirection.DESC,
            search="test",
        )

    def test_list_categories_return_error_with_invalid_sort(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Should raise an error when an invalid sort field is provided.

        When calling ListCastMember.execute with an invalid sort field,
        it should raise a ValueError.

        Args:
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = create_autospec(CastMemberRepository)
        repository.search.return_value = [
            actor,
            director,
        ]

        list_cast_member = ListCastMember(repository)

        with pytest.raises(ValueError):
            list_cast_member.execute(
                params=ListCastMemberInput(
                    sort="invalid_field",  # type: ignore
                )
            )
