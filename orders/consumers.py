import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from orders.models import Order
from orders.serializers import OrderSerializer
from users.models import User


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.location_id = self.scope["url_route"]["kwargs"]["location_id"]
        self.room_group_name = f"chat_{self.location_id}"
        self.user = await self.get_user()

        # user permissions
        if not (self.user.is_staff or self.user.is_admin):
            await self.close(code=4002)
            return

        pending_orders = await self.get_pending_orders()

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({"pending_orders": pending_orders}))

    @database_sync_to_async
    def get_user(self):
        return User.objects.get(
            id=parse_qs(self.scope["query_string"].decode("utf-8")).get("user_id")[0]
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        pending_orders = await self.get_pending_orders()

        # Send pending_orders to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "receive.orders", "pending_orders": pending_orders},
        )

    @database_sync_to_async
    def get_pending_orders(self):
        pending_orders_queryset = Order.objects.filter(
            location_id=self.location_id,
            is_paid=True,
            is_prepared=False,
        )
        serializer = OrderSerializer(pending_orders_queryset, many=True)
        return serializer.data

    # Receive pending_orders from room group
    async def receive_orders(self, event):
        pending_orders = event["pending_orders"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"pending_orders": pending_orders}))