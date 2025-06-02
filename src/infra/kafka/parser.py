import json
import logging
from dataclasses import dataclass
from typing import Type

from src._shared.domain.entity import Entity
from src._shared.models.enums import Operation
from src.domain.cast_member import CastMember
from src.domain.category import Category
from src.domain.genre import Genre
from src.domain.video import Video

logger = logging.getLogger(__name__)


@dataclass
class ParsedEvent:
    """
    Parsed event from Debezium.
    """

    entity: Type[Entity]
    operation: Operation
    payload: dict


table_to_entity = {
    "categories": Category,
    "cast_members": CastMember,
    "genres": Genre,
    "videos": Video,
}


def parse_debezium_message(data: bytes) -> ParsedEvent | None:
    """
    Parse a Debezium message from Kafka.

    Args:
    - data (bytes): The message from Kafka.

    Returns:
    - ParsedEvent | None: The parsed event, or None if the message is invalid.
    """

    try:
        json_data = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as e:
        logger.error(e)
        return None

    try:
        entity = table_to_entity[json_data["payload"]["source"]["table"]]
        operation = Operation(json_data["payload"]["op"])
        payload = (
            json_data["payload"]["after"]
            if operation != Operation.DELETE
            else json_data["payload"]["before"]
        )
    except (KeyError, ValueError) as e:
        logger.error(e)
        return None

    return ParsedEvent(entity=entity, operation=operation, payload=payload)
