from unittest.mock import MagicMock, create_autospec

import pytest
from pytest_mock import MockFixture

from src._shared.infra.kafka.event_handler import AbstractEventHandler
from src._shared.models.enums import Operation
from src.domain.category import Category
from src.infra.kafka.parser import ParsedEvent


@pytest.fixture
def consumer_logger(mocker: MockFixture) -> MagicMock:
    """
    A fixture to mock the consumer logger.

    Returns a MagicMock that can be used as a substitute for the logger in
    tests.
    """
    return mocker.patch("src._shared.infra.kafka.event_handler.logger")


class FakeHandler(AbstractEventHandler):
    """
    A fake event handler for testing purposes.
    """

    def handle_updated(self, event: ParsedEvent) -> None:
        """
        Handles an updated event.

        Args:
            event (ParsedEvent): The event containing the updated entity's payload.

        Should be implemented by subclasses to perform the necessary logic when an
        entity is updated.
        """

    def handle_deleted(self, event: ParsedEvent) -> None:
        """
        Handles a deleted event.

        Args:
            event (ParsedEvent): The event containing the deleted entity's payload.

        Should be implemented by subclasses to perform the necessary logic when an
        entity is deleted.
        """

    def handle_created(self, event: ParsedEvent) -> None:
        """
        Handles a created event.

        Args:
            event (ParsedEvent): The event containing the created entity's payload.

        Should be implemented by subclasses to perform the necessary logic when a
        new entity is created.
        """


class TestAbstractEventHandler:
    """
    Tests for the AbstractEventHandler class.
    """

    def test_when_operation_is_create_then_call_handle_created(self):
        """
        When the operation is CREATE, the handler should call handle_created with the
        event.
        """

        event = ParsedEvent(
            entity=Category,
            operation=Operation.CREATE,
            payload={"key": "value"},
        )
        handler = FakeHandler()
        handler.handle_created = create_autospec(handler.handle_created)
        handler(event)

        handler.handle_created.assert_called_once_with(event)  # type: ignore

    def test_when_operation_is_update_then_call_handle_updated(self):
        """
        When the operation is UPDATE, the handler should call handle_updated with the
        event.
        """

        event = ParsedEvent(
            entity=Category,
            operation=Operation.UPDATE,
            payload={"key": "value"},
        )
        handler = FakeHandler()
        handler.handle_updated = create_autospec(handler.handle_updated)
        handler(event)

        handler.handle_updated.assert_called_once_with(event)  # type: ignore

    def test_when_operation_is_delete_then_call_handle_deleted(self):
        """
        When the operation is DELETE, the handler should call handle_deleted with the
        event.
        """

        event = ParsedEvent(
            entity=Category,
            operation=Operation.DELETE,
            payload={"key": "value"},
        )
        handler = FakeHandler()
        handler.handle_deleted = create_autospec(handler.handle_deleted)
        handler(event)

        handler.handle_deleted.assert_called_once_with(event)  # type: ignore

    def test_when_operation_is_unknown_then_log_info(self, mocker):
        """
        When the operation is unknown, the handler should log an info message with the
        unknown operation.
        """

        event = ParsedEvent(
            entity=Category,
            operation="unknown",  # type: ignore
            payload={"key": "value"},
        )

        handler = FakeHandler()
        logger = mocker.patch("src._shared.infra.kafka.event_handler.logger")
        handler(event)

        logger.info.assert_called_once_with("Unknown operation: %s", event.operation)
