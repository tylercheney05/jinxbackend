from rest_framework import serializers

from menuitems.serializers import MenuItemDetailSerializer
from orders.models import OrderItemMenuItem


class OrderItemMenuItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemDetailSerializer(read_only=True)

    class Meta:
        model = OrderItemMenuItem
        fields = ["id", "menu_item", "price"]
        read_only_fields = ["id", "price"]
