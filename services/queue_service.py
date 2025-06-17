import json
import logging
from typing import Awaitable, Callable
import redis.asyncio as redis
from dotenv import load_dotenv
from configs.app_config import AppConfig

load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


class QueueService:
    def __init__(self):
        logger.info("[Queue] Initializing QueueService")
        self.redis_client = redis.from_url(AppConfig.get_redis_connection_string())
        logger.debug("[Queue] Connected to Redis")
        self.subscribers: dict[str, set[Awaitable[Callable]]] = {}

    def key_with_prefix(self, key: str) -> str:
        return f"{AppConfig.get_queue_exchange_name()}.{key}"

    async def publish(self, topic_key: str, data: dict):
        topic = self.key_with_prefix(topic_key)
        logger.info(
            f'[Queue] Publishing message to topic "{topic}": %s',
            data,
        )
        await self.redis_client.lpush(topic, json.dumps(data))

    def add_subscriber(self, topic_key: str):
        def decorator(callback: Awaitable[Callable]):
            topic = self.key_with_prefix(topic_key)
            logger.info(f'[Queue] Adding subscriber for topic "{topic}"')

            if topic not in self.subscribers:
                self.subscribers[topic] = set()
                logger.info(f'[Queue] Created new subscriber set for topic "{topic}"')

            handlers = self.subscribers[topic]
            handlers.add(callback)
            logger.info(
                f'[Queue] Successfully added subscriber to topic "{topic}". Total subscribers: {len(handlers)}'
            )
            return callback

        return decorator

    async def subscribe(self):
        logger.info("[Queue] Starting subscription service")

        while True:
            for topic in self.subscribers.keys():
                logger.info(f'[Queue] Waiting for messages on topic "{topic}"')

                _, data = await self.redis_client.brpop(topic)

                if not data:
                    logger.info(
                        f'[Queue] No data received for topic "{topic}", continuing...'
                    )
                    continue

                logger.info(f'[Queue] Received message from topic "{topic}": %s', data)

                callbacks = self.subscribers.get(topic)
                if not callbacks:
                    logger.warn(
                        f'[Queue] No handlers found for topic "{topic}", skipping...'
                    )
                    continue

                logger.info(
                    f'[Queue] Processing message with {len(callbacks)} handler(s) for topic "{topic}"'
                )

                for callback in callbacks:
                    try:
                        parsed_data = json.loads(data)
                        logger.info(
                            f'[Queue] Executing handler for topic "{topic}" with data: %s',
                            parsed_data,
                        )
                        await callback(parsed_data)
                        logger.info(
                            f'[Queue] Successfully processed message for topic "{topic}"'
                        )
                    except Exception as e:
                        logger.error(
                            f'[Queue] Error processing message for topic "{topic}": %s',
                            {
                                "error": str(e),
                                "stack": getattr(e, "__traceback__", None),
                                "data": data,
                            },
                        )
