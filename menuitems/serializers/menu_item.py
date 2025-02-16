from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from menuitems.models import LimitedTimePromotion, MenuItem, MenuItemFlavor
from menuitems.serializers.limited_time_menu_item import LimitedTimeMenuItemSerializer
from menuitems.serializers.menu_item_flavor import (
    MenuItemFlavorDetailSerializer,
    MenuItemFlavorSerializer,
    MenuItemFlavorSummarySerializer,
)
from sodas.serializers import SodaSerializer


class AddMenuItemFlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemFlavor
        fields = ["flavor", "quantity"]


class MenuItemSerializer(serializers.ModelSerializer):
    menu_item_flavors = serializers.ListField(
        child=AddMenuItemFlavorSerializer(), write_only=True
    )
    limited_time_promo = serializers.PrimaryKeyRelatedField(
        queryset=LimitedTimePromotion.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "soda",
            "menu_item_flavors",
            "limited_time_promo",
        ]
        read_only_fields = ["id"]

    def validate_menu_item_flavors(self, value):
        if not value:
            raise serializers.ValidationError("Menu item flavors are required.")
        return value

    def create(self, validated_data):
        flavors = validated_data.pop("menu_item_flavors")
        limited_time_promo = validated_data.pop("limited_time_promo", None)

        # Create menu item
        menu_item = MenuItem.objects.create(**validated_data)

        # Create menu item flavors
        for flavor in flavors:
            data = {
                "menu_item": menu_item.id,
                "flavor": flavor["flavor"].id,
                "quantity": flavor["quantity"],
            }
            menu_item_flavor = MenuItemFlavorSerializer(data=data)
            if menu_item_flavor.is_valid():
                menu_item_flavor.save()
            else:
                raise serializers.ValidationError(menu_item_flavor.errors)

        # Create limited time menu item
        if limited_time_promo:
            data = {
                "menu_item": menu_item.id,
                "limited_time_promo": limited_time_promo.id,
            }
            limited_time_menu_item = LimitedTimeMenuItemSerializer(data=data)
            if limited_time_menu_item.is_valid():
                limited_time_menu_item.save()
            else:
                raise serializers.ValidationError(limited_time_menu_item.errors)
        return menu_item


class MenuItemDetailSerializer(ReadOnlyModelSerializer):
    soda = SodaSerializer()
    flavors = MenuItemFlavorDetailSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "soda", "flavors"]


class MenuItemSummarySerializer(ReadOnlyModelSerializer):
    flavors = MenuItemFlavorSummarySerializer(many=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "flavors", "cup_prices"]
