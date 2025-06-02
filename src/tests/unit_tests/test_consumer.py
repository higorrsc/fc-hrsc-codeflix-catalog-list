from unittest.mock import MagicMock, create_autospec

import pytest
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaException, Message
from pytest_mock import MockFixture

from src.domain.category import Category
from src.infra.kafka.consumer import Consumer
from src.infra.kafka.parser import parse_debezium_message


@pytest.fixture
def consumer() -> Consumer:
    """
    Fixture that provides a Consumer instance with a mocked KafkaConsumer client.

    Returns:
        Consumer: An instance of the Consumer class initialized with a mock KafkaConsumer
        client and the parse_debezium_message parser.
    """

    client = create_autospec(KafkaConsumer)
    return Consumer(client=client, parser=parse_debezium_message)


@pytest.fixture
def error_message() -> Message:
    """
    Fixture that provides a Message instance with an error.

    Returns:
        Message: A Message instance with an error.
    """

    message = create_autospec(Message)
    message.error.return_value = "error"
    return message


@pytest.fixture
def empty_message() -> Message:
    """
    Fixture that provides a Kafka message with no data.

    The message is a mock object with the error attribute set to None and the value
    attribute set to None.

    Returns:
        Message: A Message instance with no payload.
    """

    message = create_autospec(Message)
    message.error.return_value = None
    message.value.return_value = None
    return message


@pytest.fixture
def message_with_invalid_data() -> Message:
    """
    Fixture that provides a Kafka message with invalid data.

    The message is a mock object with the value attribute set to a bytes object
    containing invalid JSON data (b"not a json data"). The error attribute is
    set to None.

    Returns:
        Message: A Message instance containing a payload that cannot be parsed as JSON.
    """
    message = create_autospec(Message)
    message.error.return_value = None
    message.value.return_value = b"not a json data"
    return message


@pytest.fixture
def message_with_create_data() -> Message:
    """
    Fixture that provides a Kafka message with valid create operation data.

    Returns:
        Message: A Message instance containing a payload that represents a create operation
        for a category entity with predefined attributes.
    """

    message = create_autospec(Message)
    message.error.return_value = None
    message.value.return_value = b'{"payload": {"source": {"table": "categories"}, "op": "c", "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}}}'
    return message


@pytest.fixture
def consumer_logger(mocker: MockFixture) -> MagicMock:
    """
    A fixture to mock the consumer logger.

    Returns a MagicMock that can be used as a substitute for the logger in tests.
    """

    return mocker.patch("src._shared.infra.kafka.event_handler.logger")


class TestConsume:
    """
    A class to test the consume method of the Consumer class.
    """

    def test_when_no_message_is_available_in_poll_then_return_none(
        self,
        consumer: Consumer,
    ) -> None:
        """
        When no message is available in the poll, the consume method should return None.

        This test ensures that the consumer does not hang indefinitely when no messages
        are available in the topic.
        """

        consumer.client.poll.return_value = None

        assert consumer.consume() is None

    def test_when_message_has_error_then_log_error_and_return_none(
        self,
        consumer: Consumer,
        error_message: Message,
        consumer_logger: MagicMock,
    ) -> None:
        """
        Test that when a message with an error is received, the error is logged
        and None is returned.

        This test ensures that the consumer logs the error message and returns None
        when the polled message contains an error.
        """

        consumer.client.poll.return_value = error_message

        assert consumer.consume() is None
        consumer_logger.error.assert_called_once_with(
            "received message with error: error"
        )

    def test_when_message_data_is_empty_then_return_none(
        self,
        consumer: Consumer,
        empty_message: Message,
        consumer_logger: MagicMock,
    ) -> None:
        """
        When the message data is empty, the consume method should return None.

        This test ensures that the consumer returns None when the polled message
        contains no data.
        """

        consumer.client.poll.return_value = empty_message

        assert consumer.consume() is None
        consumer_logger.assert_not_called()

    def test_when_cannot_parse_message_data_then_log_error_and_return_none(
        self,
        consumer: Consumer,
        message_with_invalid_data: Message,
        consumer_logger: MagicMock,
    ) -> None:
        """
        Test that when message data cannot be parsed, the error is logged and
        None is returned.

        This test ensures that the consumer logs the received message data and
        the parsing failure, and returns None when the message data is invalid.
        """

        consumer.client.poll.return_value = message_with_invalid_data

        assert consumer.consume() is None
        consumer_logger.info.assert_called_once_with(
            "Received message with data: b'not a json data'"
        )
        consumer_logger.error.assert_called_once_with(
            "Failed to parse message data: b'not a json data'"
        )

    def test_when_message_data_is_valid_then_parse_and_call_handler(
        self,
        consumer: Consumer,
        message_with_create_data: Message,
        mocker: MockFixture,
    ) -> None:
        """
        When the message data is valid, the consume method should parse the message data
        and call the appropriate event handler with the parsed event.

        This test ensures that the consumer parses the received message data and calls
        the appropriate event handler with the parsed event when the message data is valid.
        """
        consumer.client.poll.return_value = message_with_create_data
        mock_handler = mocker.MagicMock()
        consumer.router = {Category: mock_handler}  # type: ignore

        consumer.consume()

        mock_handler.assert_called_once()

        consumer.client.commit.assert_called_once_with(message=message_with_create_data)


class TestStart:
    """
    A class to test the start method of the Consumer class.
    """

    def test_consume_message_until_keyboard_interruption(
        self,
        consumer: Consumer,
        mocker: MockFixture,
    ) -> None:
        """
        Tests that the start method consumes messages until a KeyboardInterrupt is received.

        The test mocks the consume method to return None on the first call and raise a
        KeyboardInterrupt on the second call. It then calls the start method and asserts
        that the consume method was called twice and the client was closed.

        This test ensures that the consumer starts consuming messages until a KeyboardInterrupt
        is received.
        """

        consumer.consume = mocker.MagicMock(side_effect=[None, KeyboardInterrupt])
        consumer.start()

        assert consumer.consume.call_count == 2
        consumer.client.close.assert_called_once()

    def test_consume_message_until_kafka_exception(
        self,
        consumer: Consumer,
        mocker: MockFixture,
    ) -> None:
        """
        Test that when a KafkaException is received, the consumer stops consuming
        messages and closes the Kafka client.

        This test ensures that the consumer stops consuming messages and closes the
        Kafka client when a KafkaException is received.
        """

        consumer.consume = mocker.MagicMock(side_effect=[None, KafkaException("error")])
        consumer.start()

        assert consumer.consume.call_count == 2
        consumer.client.close.assert_called_once()
