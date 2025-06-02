import logging
from abc import ABC, abstractmethod

from src._shared.models.enums import Operation
from src.infra.kafka.parser import ParsedEvent

logger = logging.getLogger(__name__)


class AbstractEventHandler(ABC):
    """
    Abstract base class for event handlers.
    """

    @abstractmethod
    def handle_created(self, event: ParsedEvent) -> None:
        """
        Handles a created event.

        Args:
            event (ParsedEvent): The event containing the created entity's payload.

        Should be implemented by subclasses to perform the necessary logic when a
        new entity is created.
        """

        raise NotImplementedError

    @abstractmethod
    def handle_updated(self, event: ParsedEvent) -> None:
        """
        Handles an updated event.

        Args:
            event (ParsedEvent): The event containing the updated entity's payload.

        Should be implemented by subclasses to perform the necessary logic when an
        entity is updated.
        """

        raise NotImplementedError

    @abstractmethod
    def handle_deleted(self, event: ParsedEvent) -> None:
        """
        Handles a deleted event.

        Args:
            event (ParsedEvent): The event containing the deleted entity's payload.

        Should be implemented by subclasses to perform the necessary logic when an
        entity is deleted.
        """

        raise NotImplementedError

    def __call__(self, event: ParsedEvent) -> None:
        """
        Dispatches the parsed event to the appropriate handler method based on the operation type.

        Args:
            event (ParsedEvent): The event containing the payload and operation type.

        The operation type determines which handler method is called:
        - Operation.CREATE: Calls handle_created(event).
        - Operation.UPDATE: Calls handle_updated(event).
        - Operation.DELETE: Calls handle_deleted(event).

        If the operation type is unknown, logs an informational message.
        """

        if event.operation == Operation.CREATE:
            self.handle_created(event)
        elif event.operation == Operation.UPDATE:
            self.handle_updated(event)
        elif event.operation == Operation.DELETE:
            self.handle_deleted(event)
        else:
            logger.info("Unknown operation: %s", event.operation)
