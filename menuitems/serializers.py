from rest_framework import serializers

from menuitems.models import (
    LimitedTimeMenuItem,
    LimitedTimePromotion,
    MenuItem,
    MenuItemFlavor,
    MenuItemPrice,
)


class MenuItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemPrice
        fields = ["id", "price"]
        read_only_fields = ["id"]


class MenuItemFlavorSerializer(serializers.ModelSerializer):
    flavor__name = serializers.CharField(source="flavor.name", read_only=True)
    flavor__flavor_group__uom__display = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = MenuItemFlavor
        fields = [
            "flavor__name",
            "quantity",
            "flavor__flavor_group__uom__display",
            "flavor",
        ]

    def get_flavor__flavor_group__uom__display(self, obj):
        return obj.flavor.flavor_group.get_uom_display()


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
    price = MenuItemPriceSerializer(required=False, allow_null=True)

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
            "price",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        flavors = validated_data.pop("menu_item_flavors")
        limited_time_promo = validated_data.pop("limited_time_promo", None)
        price = validated_data.pop("price", None)

        menu_item = MenuItem.objects.create(**validated_data)
        for flavor in flavors:
            MenuItemFlavor.objects.create(
                menu_item=menu_item,
                flavor_id=flavor["flavor"],
                quantity=flavor["quantity"],
            )
        if limited_time_promo:
            LimitedTimeMenuItem.objects.create(
                menu_item=menu_item, limited_time_promo_id=limited_time_promo
            )
        if price:
            price_serializer = MenuItemPriceSerializer(data=price)
            price_serializer.is_valid(raise_exception=True)
            price_serializer.save(menu_item=menu_item)
        return menu_item


class LimitedTimePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LimitedTimePromotion
        fields = ["id", "name", "is_archived"]
        read_only_fields = ["id"]
