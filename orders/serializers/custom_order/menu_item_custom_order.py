from rest_framework import serializers

from orders.models import MenuItemCustomOrder
from orders.serializers import CustomOrderFlavorMenuItemCustomOrderSerializer
from sodas.serializers import SodaSerializer


class MenuItemCustomOrderSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    soda = SodaSerializer(read_only=True)
    menu_item_custom_order_custom_order_flavors = (
        CustomOrderFlavorMenuItemCustomOrderSerializer(many=True)
    )

    class Meta:
        model = MenuItemCustomOrder
        fields = [
            "id",
            "name",
            "soda",
            "menu_item_custom_order_custom_order_flavors",
        ]
        read_only_fields = ["id"]

    def get_name(self, obj):
        menu_item_custom_order_custom_order_flavors = (
            obj.menu_item_custom_order_custom_order_flavors.all()
        )
        flavors = [
            menu_item_custom_order_custom_order_flavor.custom_order_flavor.flavor.name
            for menu_item_custom_order_custom_order_flavor in menu_item_custom_order_custom_order_flavors
        ]
        if len(flavors) > 1:
            flavor_names = ", ".join(flavors[:-1]) + " and " + flavors[-1]
        else:
            flavor_names = flavors[0] if flavors else ""
        return f"{obj.menu_item.name} (Customized): {obj.soda.name} with {flavor_names}"
