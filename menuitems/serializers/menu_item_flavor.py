from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.serializers import FlavorDetailSerializer, FlavorSummarySerializer
from menuitems.models import MenuItemFlavor


class MenuItemFlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemFlavor
        fields = ["id", "menu_item", "flavor", "quantity"]


class MenuItemFlavorDetailSerializer(ReadOnlyModelSerializer):
    flavor = FlavorDetailSerializer()

    class Meta:
        model = MenuItemFlavor
        fields = ["id", "flavor", "quantity"]


class MenuItemFlavorSummarySerializer(ReadOnlyModelSerializer):
    flavor = FlavorSummarySerializer()

    class Meta:
        model = MenuItemFlavor
        fields = [
            "id",
            "flavor",
            "quantity",
        ]
