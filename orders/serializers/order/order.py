from rest_framework import serializers

from orders.models import Order
from orders.serializers import OrderItemDetailSerializer

from .order_name import OrderNameSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_name__name = serializers.CharField(source="order_name.name", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "collected_by",
            "location",
            "order_name",
            "order_name__name",
            "is_in_progress",
            "is_complete",
            "is_paid",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "is_paid": {
                "required": False,
            },
            "order_name": {
                "required": False,
            },
        }


class OrderDetailSerializer(serializers.ModelSerializer):
    order_name = OrderNameSerializer(read_only=True)
    order_items = OrderItemDetailSerializer(many=True, read_only=True, source="items")

    class Meta:
        model = Order
        fields = [
            "id",
            "order_name",
            "order_items",
            "pending_price",
        ]

        read_only_fields = ["id", "pending_price"]
