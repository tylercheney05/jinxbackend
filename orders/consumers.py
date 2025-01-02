import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import BooleanField, Case, F, IntegerField, Value, When

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
        text_data_json = json.loads(text_data)

        order_in_progress_exists = "order_in_progress" in text_data_json
        order_in_progress = text_data_json.get("order_in_progress", False)

        order_complete_exists = "order_complete" in text_data_json
        order_complete = text_data_json.get("order_complete", False)

        delete_order_exists = "delete_order" in text_data_json
        delete_order = text_data_json.get("delete_order", False)

        order_id = text_data_json.get("order_id", False)

        if order_in_progress_exists and order_id:
            await self.mark_order_in_progress(order_id, order_in_progress)

        if order_complete_exists and order_id:
            await self.mark_order_complete(order_id, order_complete)

        if delete_order_exists and delete_order and order_id:
            await self.delete_order(order_id)

        pending_orders = await self.get_pending_orders()

        # Send pending_orders to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "receive.orders", "pending_orders": pending_orders},
        )

    @database_sync_to_async
    def get_pending_orders(self):
        pending_orders_queryset = (
            Order.objects.filter(
                location_id=self.location_id,
                is_paid=True,
            )
            .annotate(
                is_complete_order=Case(
                    When(is_complete=True, then=Value(1)),
                    When(is_complete=False, then=Value(0)),
                    output_field=BooleanField(),
                ),
                order_id=Case(
                    When(is_complete=True, then=-F("id")),
                    When(is_complete=False, then=F("id")),
                    output_field=IntegerField(),
                ),
            )
            .order_by("is_complete_order", "order_id")[:10]
        )

        serializer = OrderSerializer(pending_orders_queryset, many=True)
        return serializer.data

    @database_sync_to_async
    def mark_order_in_progress(self, order_id, order_in_progress):
        order = Order.objects.get(id=order_id)
        order.is_in_progress = order_in_progress
        order.save()

    @database_sync_to_async
    def mark_order_complete(self, order_id, order_complete):
        order = Order.objects.get(id=order_id)
        order.is_complete = order_complete
        order.save()

    @database_sync_to_async
    def delete_order(self, order_id):
        Order.objects.get(id=order_id).delete()

    # Receive pending_orders from room group
    async def receive_orders(self, event):
        pending_orders = event["pending_orders"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"pending_orders": pending_orders}))
