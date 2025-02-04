from rest_framework import serializers

from orders.models import OrderItemCustomOrder
from orders.serializers.custom_order.custom_order import CustomOrderSerializer


class OrderItemCustomOrderSerializer(serializers.ModelSerializer):
    custom_order = CustomOrderSerializer(read_only=True)

    class Meta:
        model = OrderItemCustomOrder
        fields = [
            "id",
            "custom_order",
            "price",
        ]
        read_only_fields = ["id", "price"]
