from rest_framework import serializers

from orders.models import OrderItemMenuItemCustomOrder
from orders.serializers import MenuItemCustomOrderSerializer


class OrderItemMenuItemCustomOrderSerializer(serializers.ModelSerializer):
    menu_item_custom_order = MenuItemCustomOrderSerializer(read_only=True)

    class Meta:
        model = OrderItemMenuItemCustomOrder
        fields = ["id", "menu_item_custom_order", "price"]
        read_only_fields = ["id", "price"]
