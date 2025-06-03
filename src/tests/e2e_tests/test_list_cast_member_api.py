from typing import Iterator

import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient

from src.domain.cast_member import CastMember
from src.domain.cast_member_repository import CastMemberRepository
from src.infra.api._shared.dependencies import get_cast_member_repository
from src.infra.api.main import app
from src.infra.elasticsearch.elasticsearch_cast_member_repository import (
    ElasticsearchCastMemberRepository,
)


@pytest.fixture
def populated_cast_member_repository(
    populated_es: Elasticsearch,
) -> Iterator[CastMemberRepository]:
    """
    Fixture to provide a CastMemberRepository instance populated with test data.

    This fixture creates a CastMemberRepository instance backed by an Elasticsearch
    client that has been pre-populated with test cast_members. It is used to inject
    a repository with data for testing purposes.

    Args:
        populated_es (Elasticsearch): The Elasticsearch client fixture pre-populated
                                      with test cast_members.

    Yields:
        Iterator[CastMemberRepository]: A repository instance with pre-populated cast_members.
    """

    yield ElasticsearchCastMemberRepository(client=populated_es)


@pytest.fixture
def test_client_with_populated_repo(
    populated_cast_member_repository: CastMemberRepository,
) -> Iterator[TestClient]:
    """
    Fixture to provide a FastAPI TestClient instance with a populated CastMemberRepository.

    This fixture creates a TestClient instance that is configured to use the
    populated_cast_member_repository fixture for the ListCastMember use case. It is
    used to test the ListCastMember API endpoint with pre-populated cast members.

    Args:
        populated_cast_member_repository (CastMemberRepository): A CastMemberRepository
            instance pre-populated with test cast members.

    Yields:
        Iterator[TestClient]: A TestClient instance with a populated repository.
    """

    app.dependency_overrides[get_cast_member_repository] = (
        lambda: populated_cast_member_repository
    )
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_cast_members(
    test_client_with_populated_repo: TestClient,
    director: CastMember,
    actor: CastMember,
) -> None:
    """
    Should return a list of cast members with default pagination values.

    When calling the "/cast_members" endpoint, it should return a list of cast members
    with the default pagination values. The test uses a TestClient instance with
    a populated CastMemberRepository instance to test the ListCastMember API
    endpoint.

    Args:
        test_client_with_populated_repo (TestClient): A TestClient instance with
            a populated CastMemberRepository instance.
        director (CastMember): A CastMember instance representing a director cast_member.
        actor (CastMember): A CastMember instance representing a actor cast_member.

    Returns:
        None
    """

    response = test_client_with_populated_repo.get("/cast_members")
    assert response.status_code == 200
    assert response.json() == {
        "data": [
            {
                "id": str(director.id),
                "name": director.name,
                "type": director.type,
                "created_at": director.created_at.isoformat(),
                "updated_at": director.updated_at.isoformat(),
                "is_active": director.is_active,
            },
            {
                "id": str(actor.id),
                "name": actor.name,
                "type": actor.type,
                "created_at": actor.created_at.isoformat(),
                "updated_at": actor.updated_at.isoformat(),
                "is_active": actor.is_active,
            },
        ],
        "meta": {
            "page": 1,
            "per_page": 5,
            "sort": "name",
            "direction": "asc",
        },
    }
