from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from menuitems.models import MenuItem
from menuitems.serializers.limited_time_menu_item import LimitedTimeMenuItemSerializer
from menuitems.serializers.menu_item_flavor import (
    MenuItemFlavorSerializer,
    MenuItemFlavorSerializerReadOnly,
)
from menuitems.serializers.menu_item_price import MenuItemPriceSerializer
from sodas.serializers import SodaSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    flavors = MenuItemFlavorSerializer(many=True)
    limited_time_menu_item = LimitedTimeMenuItemSerializer(
        required=False, allow_null=True
    )
    price = MenuItemPriceSerializer(required=False, allow_null=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "soda", "flavors", "limited_time_menu_item", "price"]

    def validate_flavors(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError("At least one flavor must be provided.")
        return value

    def create(self, validated_data):
        flavors = validated_data.pop("flavors", [])
        limited_time_menu_item = validated_data.pop("limited_time_menu_item", None)
        price = validated_data.pop("price", None)

        menu_item = super().create(validated_data)
        for flavor in flavors:
            menu_item_flavor_serializer = MenuItemFlavorSerializer(
                data={
                    **flavor,
                    "flavor": flavor.get("flavor").id,
                }
            )
            menu_item_flavor_serializer.is_valid(raise_exception=True)
            menu_item_flavor_serializer.save(menu_item=menu_item)
        if limited_time_menu_item:
            limited_time_menu_item_serializer = LimitedTimeMenuItemSerializer(
                data={
                    **limited_time_menu_item,
                    "limited_time_promo": limited_time_menu_item.get(
                        "limited_time_promo"
                    ).id,
                }
            )
            limited_time_menu_item_serializer.is_valid(raise_exception=True)
            limited_time_menu_item_serializer.save(menu_item=menu_item)

        if price:
            price_serializer = MenuItemPriceSerializer(data=price)
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save(menu_item=menu_item)
        return menu_item


class MenuItemSerializerReadOnly(ReadOnlyModelSerializer):
    soda = SodaSerializer()
    flavors = MenuItemFlavorSerializerReadOnly(many=True)

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "soda",
            "flavors",
            "cup_prices",
        ]
