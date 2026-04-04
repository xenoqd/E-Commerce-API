from backend.modules.order.service import OrderService


class OrderCreatedHandler:
    def __init__(self, order_service: OrderService):
        self.order_service = order_service

    async def handle(self, msg_id: str, event_type: str, data: dict):
        print(f"[EVENT] Processing ORDER_CREATED: order_id={data.get('order_id')}")

        try:
            await self.order_service.process_order_created(
                order_id=data["order_id"], user_id=data["user_id"]
            )
        except Exception as e:
            print(f"[ERROR] Failed to process order {data.get('order_id')}: {e}")
            raise
