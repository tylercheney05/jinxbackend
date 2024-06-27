from rest_framework import serializers

from menuitems.models import MenuItem, MenuItemFlavor


class MenuItemFlavorSerializer(serializers.ModelSerializer):
    flavor__name = serializers.CharField(source="flavor.name", read_only=True)
    flavor__flavor_group__uom__display = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = MenuItemFlavor
        fields = ["flavor__name", "quantity", "flavor__flavor_group__uom__display"]

    def get_flavor__flavor_group__uom__display(self, obj):
        return obj.flavor.flavor_group.get_uom_display()


class MenuItemSerializer(serializers.ModelSerializer):
    menu_item_flavors = serializers.ListField(
        child=serializers.DictField(), write_only=True
    )
    flavors = MenuItemFlavorSerializer(many=True, read_only=True)
    soda__name = serializers.CharField(source="soda.name", read_only=True)
    cup_prices = serializers.DictField(read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            "name",
            "soda",
            "soda__name",
            "flavors",
            "menu_item_flavors",
            "cup_prices",
        ]

    def create(self, validated_data):
        flavors = validated_data.pop("menu_item_flavors")
        menu_item = MenuItem.objects.create(**validated_data)
        for flavor in flavors:
            MenuItemFlavor.objects.create(
                menu_item=menu_item,
                flavor_id=flavor["flavor"],
                quantity=flavor["quantity"],
            )
        return menu_item
