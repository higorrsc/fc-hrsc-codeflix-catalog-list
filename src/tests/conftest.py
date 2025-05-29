from datetime import datetime
from typing import Generator
from uuid import uuid4

import pytest
from elasticsearch import Elasticsearch

from src._shared.constants import (
    ELASTICSEARCH_CAST_MEMBER_INDEX,
    ELASTICSEARCH_CATEGORY_INDEX,
    ELASTICSEARCH_HOST_TEST,
)
from src.domain.cast_member import CastMember, CastMemberType
from src.domain.category import Category


@pytest.fixture
def es() -> Generator[Elasticsearch, None, None]:
    """
    Fixture to create an Elasticsearch client connected to the test instance.

    Yields a configured Elasticsearch client connected to the test instance.
    The client is configured with the test instance host and ensures that the
    index for categories exists when the fixture is used.

    After the fixture is used, the index for categories is deleted.
    """

    client = Elasticsearch(hosts=[ELASTICSEARCH_HOST_TEST])

    if not client.indices.exists(index=ELASTICSEARCH_CATEGORY_INDEX):
        client.indices.create(index=ELASTICSEARCH_CATEGORY_INDEX)
    if not client.indices.exists(index=ELASTICSEARCH_CAST_MEMBER_INDEX):
        client.indices.create(index=ELASTICSEARCH_CAST_MEMBER_INDEX)
    yield client

    client.indices.delete(index=ELASTICSEARCH_CATEGORY_INDEX)
    client.indices.delete(index=ELASTICSEARCH_CAST_MEMBER_INDEX)


@pytest.fixture
def movie() -> Category:
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
def series() -> Category:
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


@pytest.fixture
def documentary() -> Category:
    """
    Fixture that returns a Category instance representing a documentary category.

    Returns:
        Category: A Category object with predefined attributes for testing.
    """

    return Category(
        id=uuid4(),
        name="Documentários",
        description="Categoria de documentários",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def actor() -> CastMember:
    """
    Fixture that returns a CastMember instance representing an actor.

    Returns:
        CastMember: A CastMember object with predefined attributes for testing.
    """

    return CastMember(
        id=uuid4(),
        name="John Doe",
        type=CastMemberType.ACTOR,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def director() -> CastMember:
    """
    Fixture that returns a CastMember instance representing a director.

    Returns:
        CastMember: A CastMember object with predefined attributes for testing.
    """

    return CastMember(
        id=uuid4(),
        name="Jane Doe",
        type=CastMemberType.DIRECTOR,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_active=True,
    )


@pytest.fixture
def populated_es(
    es: Elasticsearch,
    movie: Category,
    series: Category,
    documentary: Category,
    actor: CastMember,
    director: CastMember,
) -> Elasticsearch:
    """
    Fixture to create an Elasticsearch client connected to the test instance
    with three categories pre-populated.

    Args:
        es (Elasticsearch): The Elasticsearch client fixture connected to the test
                            instance.
        movie (Category): A Category instance representing a movie category.
        series (Category): A Category instance representing a series category.
        documentary (Category): A Category instance representing a documentary category.

    Returns:
        Elasticsearch: The Elasticsearch client fixture connected to the test
                       instance with three categories pre-populated.
    """

    es.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(movie.id),
        body=movie.model_dump(mode="json"),
        refresh=True,
    )
    es.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(series.id),
        body=series.model_dump(mode="json"),
        refresh=True,
    )
    es.index(
        index=ELASTICSEARCH_CATEGORY_INDEX,
        id=str(documentary.id),
        body=documentary.model_dump(mode="json"),
        refresh=True,
    )
    es.index(
        index=ELASTICSEARCH_CAST_MEMBER_INDEX,
        id=str(actor.id),
        body=actor.model_dump(mode="json"),
        refresh=True,
    )
    es.index(
        index=ELASTICSEARCH_CAST_MEMBER_INDEX,
        id=str(director.id),
        body=director.model_dump(mode="json"),
        refresh=True,
    )

    return es
