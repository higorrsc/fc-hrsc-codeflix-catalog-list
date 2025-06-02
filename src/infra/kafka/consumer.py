import logging
import os
from typing import Callable, Type

from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaException

from src._shared.domain.entity import Entity
from src._shared.infra.kafka.event_handler import AbstractEventHandler
from src.domain.video import Video
from src.infra.kafka.parser import ParsedEvent, parse_debezium_message
from src.infra.kafka.video_event_handler import VideoEventHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

# Configuration for the Kafka consumer
config = {
    "bootstrap.servers": os.getenv("BOOTSTRAP_SERVERS", "kafka:19092"),
    "group.id": "consumer-cluster",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
}
topics = [
    "catalog-db.codeflix.videos",
]

# Similar to a "router" -> calls proper handler
entity_to_handler: dict[Type[Entity], Type[AbstractEventHandler]] = {
    # Category: CategoryEventHandler,
    # CastMember: CastMemberEventHandler,
    # Genre: GenreEventHandler,
    Video: VideoEventHandler,
}


class Consumer:
    """
    Kafka Consumer
    """

    def __init__(
        self,
        client: KafkaConsumer,
        parser: Callable[[bytes], ParsedEvent | None],
        router: dict[Type[Entity], Type[AbstractEventHandler]] | None = None,
    ) -> None:
        """
        Initializes a new instance of the Consumer class.

        Args:
            client (KafkaConsumer): The Kafka client to use.
            parser (Callable[[bytes], ParsedEvent | None]): The parser to use for parsing events.
            router (dict[Type[Entity], Type[AbstractEventHandler]] | None, optional): The router
            to use for calling the appropriate event handler. Defaults to the entity_to_handler
            dictionary.
        """

        self.client = client
        self.parser = parser
        self.router = router or entity_to_handler

    def start(self):
        """
        Starts consuming messages from Kafka and calls the appropriate event handler
        based on the message payload.

        The consumer will run indefinitely until a KeyboardInterrupt is received.

        If a KafkaException is received, the error will be logged and the consumer
        will stop.

        Finally, the consumer will be stopped.
        """

        logger.info("Starting consumer...")
        try:
            while True:
                self.consume()
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
        except KafkaException as e:
            logger.error(e)
        finally:
            self.stop()

    def consume(self) -> None:
        """
        Consumes a message from Kafka and calls the appropriate event handler
        based on the message payload.

        If a message is received with an error, the error will be logged and
        the function will return.

        If the message is empty, a message will be logged and the function will
        return.

        If the message cannot be parsed, an error will be logged and the function
        will return.

        Otherwise, the proper event handler will be called with the parsed event
        and the message will be committed.

        This function runs indefinitely until a KeyboardInterrupt is received.
        """

        message = self.client.poll(timeout=1.0)
        if message is None:
            logger.info("No message received")
            return None

        if message.error():
            logger.error("received message with error: %s", message.error())
            return None

        message_data = message.value()
        if not message_data:
            logger.info("Empty message received")
            return None

        logger.info("Received message with data: %s", message_data)
        parsed_event = self.parser(message_data)
        if parsed_event is None:
            logger.error("Failed to parse message data: %s", message_data)
            return None

        # Call the proper handler
        handler = self.router[parsed_event.entity]()
        handler(parsed_event)

        self.client.commit(message=message)

    def stop(self):
        """
        Stops the consumer by closing the Kafka client.
        """

        logger.info("Closing consumer...")
        self.client.close()


if __name__ == "__main__":
    kafka_consumer = KafkaConsumer(config)
    kafka_consumer.subscribe(topics=topics)
    consumer = Consumer(client=kafka_consumer, parser=parse_debezium_message)
    consumer.start()
