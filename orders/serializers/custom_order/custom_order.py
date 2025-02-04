from rest_framework import serializers

from orders.models import CustomOrder
from orders.serializers.custom_order_flavor.custom_order_flavor_custom_order import (
    CustomOrderFlavorCustomOrderSerializer,
)
from sodas.serializers import SodaSerializer


class CustomOrderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    soda = SodaSerializer(read_only=True)
    custom_order_custom_order_flavors = CustomOrderFlavorCustomOrderSerializer(
        many=True, read_only=True
    )

    class Meta:
        model = CustomOrder
        fields = ["id", "name", "soda", "custom_order_custom_order_flavors"]

    def get_name(self, obj):
        custom_order_custom_order_flavors = obj.custom_order_custom_order_flavors.all()
        flavors = [
            custom_order_custom_order_flavor.custom_order_flavor.flavor.name
            for custom_order_custom_order_flavor in custom_order_custom_order_flavors
        ]
        if len(flavors) > 1:
            flavor_names = ", ".join(flavors[:-1]) + " and " + flavors[-1]
        else:
            flavor_names = flavors[0] if flavors else ""
        finish_text = f" with {flavor_names}" if flavor_names else ""
        return f"Custom Drink: {obj.soda.name}{finish_text}"
