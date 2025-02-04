from rest_framework import serializers

from flavors.serializers import FlavorDetailSerializer
from menuitems.models import MenuItemFlavor


class MenuItemFlavorSerializer(serializers.ModelSerializer):
    flavor__name = serializers.CharField(source="flavor.name", read_only=True)
    flavor__flavor_group__uom__display = serializers.SerializerMethodField(
        read_only=True
    )
    cup_quantities = serializers.DictField(read_only=True)

    class Meta:
        model = MenuItemFlavor
        fields = [
            "flavor__name",
            "quantity",
            "flavor__flavor_group__uom__display",
            "flavor",
            "cup_quantities",
        ]

    def get_flavor__flavor_group__uom__display(self, obj):
        return obj.flavor.flavor_group.get_uom_display()


class MenuItemFlavorDetailSerializer(serializers.ModelSerializer):
    flavor = FlavorDetailSerializer(read_only=True)

    class Meta:
        model = MenuItemFlavor
        fields = ["id", "flavor", "quantity"]
