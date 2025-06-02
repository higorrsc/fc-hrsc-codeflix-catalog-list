from pytest_mock import MockFixture

from src._shared.models.enums import Operation
from src.domain.category import Category
from src.infra.kafka.parser import ParsedEvent, parse_debezium_message


class TestParseDebeziumMessage:
    """
    Test suite for the parse_debezium_message function
    """

    def test_parse_created_message(self):
        """
        Test that a Debezium message with a create operation is correctly parsed.

        This test verifies that when a Debezium message indicating a create operation
        for a category entity is passed to the `parse_debezium_message` function, it
        returns a `ParsedEvent` object with the expected entity type, operation, and
        payload. The payload contains the attributes of the category entity after the
        create operation.
        """

        data = b'{"payload": {"source": {"table": "categories"}, "op": "c", "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}}}'
        parsed_event = parse_debezium_message(data)
        expected_event = ParsedEvent(
            entity=Category,
            operation=Operation.CREATE,
            payload={
                "id": 1,
                "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006",
                "name": "Category 1",
                "description": "Description 1",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01",
                "is_active": True,
            },
        )
        assert parsed_event == expected_event

    def test_parse_updated_message(self):
        """
        Test that a Debezium message with an update operation is correctly parsed.

        This test verifies that when a Debezium message indicating an update operation
        for a category entity is passed to the `parse_debezium_message` function, it
        returns a `ParsedEvent` object with the expected entity type, operation, and
        payload. The payload contains the updated attributes of the category entity
        after the update operation.
        """

        data = b'{"payload": {"source": {"table": "categories"}, "op": "u", "before": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}, "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1 Updated", "description": "Description 1 Updated", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}}}'
        parsed_event = parse_debezium_message(data)
        expected_event = ParsedEvent(
            entity=Category,
            operation=Operation.UPDATE,
            payload={
                "id": 1,
                "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006",
                "name": "Category 1 Updated",
                "description": "Description 1 Updated",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01",
                "is_active": True,
            },
        )
        assert parsed_event == expected_event

    def test_parse_deleted_message(self):
        """
        Test that a Debezium message with a delete operation is correctly parsed.

        This test verifies that when a Debezium message indicating a delete operation
        for a category entity is passed to the `parse_debezium_message` function, it
        returns a `ParsedEvent` object with the expected entity type, operation, and
        payload. The payload contains the attributes of the category entity before the
        delete operation.
        """

        data = b'{"payload": {"source": {"table": "categories"}, "op": "d", "before": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}, "after": null }}'
        parsed_event = parse_debezium_message(data)
        expected_event = ParsedEvent(
            entity=Category,
            operation=Operation.DELETE,
            payload={
                "id": 1,
                "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006",
                "name": "Category 1",
                "description": "Description 1",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01",
                "is_active": True,
            },
        )
        assert parsed_event == expected_event

    def test_when_message_is_invalid_json_then_return_none_and_log_error(
        self,
        mocker: MockFixture,
    ):
        """
        Test that when the message is invalid JSON, the parser returns None and logs an error.

        This test verifies that the parser returns None and logs an error when the message is
        invalid JSON. The message is a bytes object containing a JSON string missing a closing
        brace. The parser should return None and log an error using the logger.error method.
        """

        log_error = mocker.patch("src.infra.kafka.parser.logger.error")
        data = b'{"payload": {"source": {"table": "categories"}, "op": "c", "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}'
        parsed_event = parse_debezium_message(data)
        assert parsed_event is None
        log_error.assert_called_once()

    def test_when_message_is_missing_required_key_then_return_none(
        self,
        mocker: MockFixture,
    ):
        """
        Test that when the message is missing a required key, the parser returns
        None and logs an error.

        This test ensures that the parser returns None and logs an error when the
        message is missing a required key.
        """

        log_error = mocker.patch("src.infra.kafka.parser.logger.error")
        data = b'{"payload": {}}'
        parsed_event = parse_debezium_message(data)
        assert parsed_event is None
        log_error.assert_called_once()
