from datetime import datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src._shared.domain.entity import Entity


class TestEntity:
    def test_entity_creation(self):
        """
        Test that an Entity instance can be created with valid attributes.
        """
        entity_id = uuid4()
        created_at = datetime.now()
        updated_at = datetime.now()
        is_active = True

        entity = Entity(
            id=entity_id,
            created_at=created_at,
            updated_at=updated_at,
            is_active=is_active,
        )

        assert entity.id == entity_id
        assert entity.created_at == created_at
        assert entity.updated_at == updated_at
        assert entity.is_active == is_active

    def test_entity_id_validation(self):
        """
        Test that the Entity id attribute is validated to be a UUID.
        """
        with pytest.raises(ValidationError):
            Entity(
                id="invalid_id",  # type: ignore
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active=True,
            )

    def test_entity_created_at_validation(self):
        """
        Test that the Entity created_at attribute is validated to be a datetime.
        """
        with pytest.raises(ValidationError):
            Entity(
                id=uuid4(),
                created_at="invalid_date",  # type: ignore
                updated_at=datetime.now(),
                is_active=True,
            )

    def test_entity_updated_at_validation(self):
        """
        Test that the Entity updated_at attribute is validated to be a datetime.
        """
        with pytest.raises(ValidationError):
            Entity(
                id=uuid4(),
                created_at=datetime.now(),
                updated_at="invalid_date",  # type: ignore
                is_active=True,
            )

    def test_entity_is_active_validation(self):
        """
        Test that the Entity is_active attribute is validated to be a boolean.
        """
        with pytest.raises(ValidationError):
            Entity(
                id=uuid4(),
                created_at=datetime.now(),
                updated_at=datetime.now(),
                is_active="invalid_bool",  # type: ignore
            )
