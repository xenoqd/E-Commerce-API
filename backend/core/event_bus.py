import json
import asyncio
from datetime import datetime
from typing import Dict, Callable, Awaitable
import redis.asyncio as redis
from redis.exceptions import ResponseError


class EventBus:
    STREAM_NAME = "ecommerce_events"

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def publish(self, event_type: str, data: dict) -> str:
        payload = {
            "type": event_type,
            "ts": datetime.utcnow().isoformat(),
            "payload": json.dumps(data, ensure_ascii=False),
        }
        msg_id = await self.redis.xadd(
            self.STREAM_NAME, payload, maxlen=1_000_000, approximate=True
        )
        return msg_id.decode() if isinstance(msg_id, bytes) else msg_id

    async def ensure_group(self, group_name: str):
        try:
            await self.redis.xgroup_create(
                self.STREAM_NAME, group_name, id=b"$", mkstream=True
            )
        except ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def consume(
        self,
        group_name: str,
        consumer_name: str,
        handler: Callable[[str, str, Dict], Awaitable[None]],
        batch_size: int = 10,
        block_ms: int = 5000,
    ):
        await self.ensure_group(group_name)

        print(f"Consumer {consumer_name} started in group {group_name}")

        while True:
            try:
                streams_dict = {self.STREAM_NAME: b">"}
                messages = await self.redis.xreadgroup(
                    group_name,
                    consumer_name,
                    streams_dict,
                    count=batch_size,
                    block=block_ms,
                )

                if not messages:
                    continue

                for _, msg_list in messages:
                    for msg_id_bytes, fields in msg_list:
                        try:
                            event_type = fields.get(b"type", b"").decode("utf-8")
                            payload_bytes = fields.get(b"payload", b"")
                            data = json.loads(payload_bytes) if payload_bytes else {}

                            await handler(msg_id_bytes.decode(), event_type, data)

                            await self.redis.xack(
                                self.STREAM_NAME, group_name, msg_id_bytes
                            )

                        except Exception as exc:
                            print(f"Handler error on {msg_id_bytes}: {exc}")

            except redis.ConnectionError:
                print("Redis disconnected, reconnecting in 3s...")
                await asyncio.sleep(3)
            except Exception as e:
                print(f"Consumer loop error: {e}")
                await asyncio.sleep(1)
