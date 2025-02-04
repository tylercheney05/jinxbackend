from rest_framework import serializers

from orders.models.custom_order_flavor import CustomOrderFlavorMenuItemCustomOrder
from orders.serializers import CustomOrderFlavorSerializer


class CustomOrderFlavorMenuItemCustomOrderSerializer(serializers.ModelSerializer):
    custom_order_flavor = CustomOrderFlavorSerializer(read_only=True)

    class Meta:
        model = CustomOrderFlavorMenuItemCustomOrder
        fields = ["id", "custom_order_flavor"]
        read_only_fields = ["id"]
