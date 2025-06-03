from unittest.mock import create_autospec

import pytest
from fastapi.testclient import TestClient

from src.domain.cast_member_repository import CastMemberRepository
from src.infra.api._shared.dependencies import get_cast_member_repository
from src.infra.api.main import app


@pytest.fixture
def client() -> TestClient:  # type: ignore
    """
    Fixture that returns a TestClient instance with a mocked CastMemberRepository.

    The fixture mocks the CastMemberRepository instance that is injected into the
    ListCastMember API endpoint. The mocked instance is replaced in the app's
    dependency overrides before the test is run, and is cleared after the test
    has finished running.

    Returns:
        TestClient: A TestClient instance with a mocked CastMemberRepository.
    """

    app.dependency_overrides[get_cast_member_repository] = lambda: create_autospec(
        CastMemberRepository
    )
    yield TestClient(app)  # type: ignore
    app.dependency_overrides.clear()


def test_categories_endpoint_with_default_pagination(client):
    """
    When calling the "/cast_members" endpoint without a pagination value, the API
    should return a 200 response with the default pagination values.

    Args:
        client (TestClient): A TestClient instance with a mocked CastMemberRepository.

    Returns:
        None
    """

    response = client.get("/cast_members")

    assert response.status_code == 200
    assert response.json()["meta"]["page"] == 1


def test_categories_endpoint_with_pagination(client):
    """
    When calling the "/cast_members" endpoint with a valid pagination value, the API
    should return a 200 response with the correct pagination values.

    Args:
        client (TestClient): A TestClient instance with a mocked CastMemberRepository.

    Returns:
        None
    """

    response = client.get("/cast_members?page=4")

    assert response.status_code == 200
    assert response.json()["meta"]["page"] == 4


def test_categories_endpoint_with_invalid_sort_field(client):
    """
    When calling the "/cast_members" endpoint with an invalid sort field, the API
    should return a 422 response.

    Args:
        client (TestClient): A TestClient instance with a mocked CastMemberRepository.

    Returns:
        None
    """

    response = client.get("/cast_members?sort=invalid_field")

    assert response.status_code == 422


def test_categories_endpoint_with_valid_sort_field(client):
    """
    When calling the "/cast_members" endpoint with a valid sort field, the API
    should return a 200 response.

    Args:
        client (TestClient): A TestClient instance with a mocked CastMemberRepository.

    Returns:
        None
    """

    response = client.get("/cast_members?sort=type")

    assert response.status_code == 200
