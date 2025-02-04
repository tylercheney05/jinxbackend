from django.apps import apps
from rest_framework import serializers

from menuitems.models import MenuItem
from menuitems.serializers import (
    MenuItemFlavorDetailSerializer,
    MenuItemFlavorSerializer,
)
from sodas.serializers import SodaSerializer


class MenuItemSerializer(serializers.ModelSerializer):
    menu_item_flavors = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )
    flavors = MenuItemFlavorSerializer(many=True, read_only=True)
    soda__name = serializers.CharField(source="soda.name", read_only=True)
    cup_prices = serializers.ListField(read_only=True)
    limited_time_promo = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = MenuItem
        fields = [
            "id",
            "name",
            "soda",
            "soda__name",
            "flavors",
            "menu_item_flavors",
            "cup_prices",
            "limited_time_promo",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        flavors = validated_data.pop("menu_item_flavors")
        limited_time_promo = validated_data.pop("limited_time_promo", None)
        menu_item = MenuItem.objects.create(**validated_data)
        for flavor in flavors:
            menu_item_flavor_model = apps.get_model("menuitems", "MenuItemFlavor")
            menu_item_flavor_model.objects.create(
                menu_item=menu_item,
                flavor_id=flavor["flavor"],
                quantity=flavor["quantity"],
            )
        if limited_time_promo:
            limited_item_menu_item_model = apps.get_model(
                "menuitems", "LimitedTimeMenuItem"
            )
            limited_item_menu_item_model.objects.create(
                menu_item=menu_item, limited_time_promo_id=limited_time_promo
            )
        return menu_item


class MenuItemDetailSerializer(serializers.ModelSerializer):
    soda = SodaSerializer(read_only=True)
    flavors = MenuItemFlavorDetailSerializer(many=True, read_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "name", "soda", "flavors"]
