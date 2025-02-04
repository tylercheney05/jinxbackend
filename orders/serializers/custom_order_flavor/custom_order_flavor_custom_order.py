from rest_framework import serializers

from orders.models import CustomOrderFlavorCustomOrder
from orders.serializers import CustomOrderFlavorSerializer


class CustomOrderFlavorCustomOrderSerializer(serializers.ModelSerializer):
    custom_order_flavor = CustomOrderFlavorSerializer(read_only=True)

    class Meta:
        model = CustomOrderFlavorCustomOrder
        fields = [
            "id",
            "custom_order_flavor",
        ]
