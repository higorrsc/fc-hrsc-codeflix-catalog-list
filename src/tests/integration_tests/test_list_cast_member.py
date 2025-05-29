from elasticsearch import Elasticsearch

from src._shared.constants import DEFAULT_PAGINATION_SIZE
from src._shared.listing import ListOutput, ListOutputMeta, SortDirection
from src.application.list_cast_member import (
    CastMemberSortableFields,
    ListCastMember,
    ListCastMemberInput,
)
from src.domain.cast_member import CastMember
from src.infra.elasticsearch.elasticsearch_cast_member_repository import (
    ElasticsearchCastMemberRepository,
)


class TestListCastMember:
    """
    Test suite for the ListCastMember use case.
    """

    def test_list_cast_members_with_default_values(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        """
        Should return a list of cast_members with default values.

        When calling ListCastMember.execute with default values, it should return a list of
        cast_members with the default values.

        Args:
            populated_es (Elasticsearch): The Elasticsearch client fixture connected to the test
                                          instance.
            actor_cast_member (CastMember): A CastMember instance representing a actor cast_member.
            director_cast_member (CastMember): A CastMember instance representing a director cast_member.

        Returns:
            None
        """
        list_cast_member = ListCastMember(
            ElasticsearchCastMemberRepository(populated_es)
        )
        output = list_cast_member.execute(ListCastMemberInput())

        assert output.data == [
            director,
            actor,
        ]
        assert output.meta == ListOutputMeta(
            page=1,
            per_page=DEFAULT_PAGINATION_SIZE,
            sort=CastMemberSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output.data) == 2

        assert output == ListOutput(
            data=[
                director,
                actor,
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=DEFAULT_PAGINATION_SIZE,
                sort=CastMemberSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

    def test_list_cast_members_with_pagination_sorting_and_search(
        self,
        populated_es: Elasticsearch,
        actor: CastMember,
    ) -> None:
        list_cast_member = ListCastMember(
            ElasticsearchCastMemberRepository(populated_es)
        )

        output_page_1 = list_cast_member.execute(
            ListCastMemberInput(
                page=1,
                per_page=1,
                sort=CastMemberSortableFields.NAME,
                direction=SortDirection.ASC,
                search="John",
            )
        )

        assert output_page_1.data == [actor]
        assert output_page_1.meta == ListOutputMeta(
            page=1,
            per_page=1,
            sort=CastMemberSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_1.data) == 1

        assert output_page_1 == ListOutput(
            data=[actor],
            meta=ListOutputMeta(
                page=1,
                per_page=1,
                sort=CastMemberSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )

        output_page_2 = list_cast_member.execute(
            ListCastMemberInput(
                page=2,
                per_page=1,
                sort=CastMemberSortableFields.NAME,
                direction=SortDirection.ASC,
                search="John",
            )
        )

        assert output_page_2.data == []
        assert output_page_2.meta == ListOutputMeta(
            page=2,
            per_page=1,
            sort=CastMemberSortableFields.NAME,
            direction=SortDirection.ASC,
        )
        assert len(output_page_2.data) == 0

        assert output_page_2 == ListOutput(
            data=[],
            meta=ListOutputMeta(
                page=2,
                per_page=1,
                sort=CastMemberSortableFields.NAME,
                direction=SortDirection.ASC,
            ),
        )
