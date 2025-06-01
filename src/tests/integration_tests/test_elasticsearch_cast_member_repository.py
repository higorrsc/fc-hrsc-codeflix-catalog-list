import logging
from unittest.mock import create_autospec
from uuid import uuid4

from elasticsearch import Elasticsearch

from src._shared.constants import ELASTICSEARCH_CAST_MEMBER_INDEX
from src._shared.listing import SortDirection
from src.application.list_cast_member import CastMemberSortableFields
from src.domain.cast_member import CastMember
from src.infra.elasticsearch.elasticsearch_cast_member_repository import (
    ElasticsearchCastMemberRepository,
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

        repository = ElasticsearchCastMemberRepository(es)
        result = repository.search()
        assert not result

    def test_when_index_has_cast_members_then_return_mapped_cast_members_with_default_search(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        When the index has cast_members, the repository should return a list of mapped
        cast_members with the default search
        """

        repository = ElasticsearchCastMemberRepository(populated_es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            actor,
            director,
        ]

    def test_when_index_has_malformed_cast_members_then_return_valid_cast_members_and_log_error(
        self,
        es: Elasticsearch,
        actor: CastMember,
    ) -> None:
        """
        When the index has malformed cast_members, the repository should return
        valid cast_members and log an error.
        """

        es.index(
            index=ELASTICSEARCH_CAST_MEMBER_INDEX,
            id=str(actor.id),
            body=actor.model_dump(mode="json"),
            refresh=True,
        )
        es.index(
            index=ELASTICSEARCH_CAST_MEMBER_INDEX,
            id=str(uuid4()),
            body={"name": "Malformed"},
            refresh=True,
        )
        mock_logger = create_autospec(logging.Logger)
        repository = ElasticsearchCastMemberRepository(client=es, logger=mock_logger)

        cast_members = repository.search()

        assert cast_members == [actor]
        mock_logger.error.assert_called_once()

    def test_when_search_term_matches_cast_member_name_then_return_matching_entities(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        When the search term matches a cast_member name, the repository should return matching
        cast_members.

        This test adds two cast_members to the Elasticsearch index, and verifies that the
        ElasticsearchCastMemberRepository returns the correct cast_members when searching for a
        term that matches a cast_member name.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = ElasticsearchCastMemberRepository(populated_es)
        result = repository.search(search="actor")
        assert result == [actor]

        result = repository.search(search="director")
        assert result == [director]

        result = repository.search(
            search="Doe",
            sort=CastMemberSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [
            director,
            actor,
        ]


class TestSort:
    """
    Test cases for sorting cast_members in the ElasticsearchCastMemberRepository
    """

    def test_when_no_sorting_is_specified_then_return_cast_members_ordered_by_insertion_order(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Test that when no sorting is specified, cast_members are returned in insertion order.

        This test adds two cast_members to the Elasticsearch index without specifying any sorting
        parameters, and verifies that the ElasticsearchCastMemberRepository returns the cast_members
        in the order they were inserted.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = ElasticsearchCastMemberRepository(populated_es)
        result = repository.search()
        assert len(result) == 2
        assert result == [
            actor,
            director,
        ]

    def test_return_cast_members_ordered_by_name_asc(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Test that when sorting by name in ascending order, cast_members are returned in the correct
        order.

        This test adds two cast_members to the Elasticsearch index, one with a name that comes
        first in a lexicographical sort and one that comes second, and verifies that the
        ElasticsearchCastMemberRepository returns the cast_members in the correct order when
        sorting by name in ascending order.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            documentary (CastMember): A CastMember instance representing a documentary cast_member.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """
        repository = ElasticsearchCastMemberRepository(populated_es)
        result = repository.search(
            sort=CastMemberSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert len(result) == 2
        assert result == [
            director,
            actor,
        ]

    def test_return_cast_members_ordered_by_name_desc(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Test that when sorting by name in descending order, cast_members are returned in the correct
        order.

        This test adds two cast_members to the Elasticsearch index, one with a name that comes
        second in a lexicographical sort and one that comes first, and verifies that the
        ElasticsearchCastMemberRepository returns the cast_members in the correct order when
        sorting by name in descending order.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            documentary (CastMember): A CastMember instance representing a documentary cast_member.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = ElasticsearchCastMemberRepository(populated_es)
        result = repository.search(
            sort=CastMemberSortableFields.NAME,  # type: ignore
            direction=SortDirection.DESC,
        )
        assert len(result) == 2
        assert result == [
            actor,
            director,
        ]


class TestPagination:
    """
    Test cases for pagination in the ElasticsearchCastMemberRepository
    """

    def test_when_no_page_is_requested_then_return_default_paginated_response(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        When no page is requested, the repository should return a default paginated response.

        When calling the search method of the ElasticsearchCastMemberRepository without
        specifying a page, it should return a list of cast_members with the default pagination
        values.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            documentary (CastMember): A CastMember instance representing a documentary cast_member.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """
        repository = ElasticsearchCastMemberRepository(populated_es)
        assert repository.search() == [
            actor,
            director,
        ]

    def test_when_page_is_requested_then_return_paginated_response(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Test that when a specific page is requested, the repository returns a paginated response.

        This test ensures that when requesting a specific page with a specified number of items
        per page, the ElasticsearchCastMemberRepository returns the correct subset of cast_members
        that belong to that page.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                        instance.
            actor (CastMember): A CastMember instance representing a actor cast_member.
            director (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """

        repository = ElasticsearchCastMemberRepository(populated_es)

        result = repository.search(
            page=1,
            per_page=1,
            sort=CastMemberSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [director]

        result = repository.search(
            page=2,
            per_page=1,
            sort=CastMemberSortableFields.NAME,  # type: ignore
            direction=SortDirection.ASC,
        )
        assert result == [actor]

    def test_when_request_page_is_out_of_bounds_then_return_empty_list(
        self,
        populated_es: Elasticsearch,
    ) -> None:
        """
        Test that when a page number is requested that is out of bounds, an empty list is returned.

        This test ensures that when requesting a page that is out of bounds, the
        ElasticsearchCastMemberRepository returns an empty list.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                        instance.

        Returns:
            None
        """

        repository = ElasticsearchCastMemberRepository(populated_es)
        assert not repository.search(page=2)
