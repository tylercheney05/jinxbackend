from rest_framework import serializers

from core.serializers import ReadOnlyModelSerializer
from flavors.serializers.flavor import FlavorSerializerReadOnly
from menuitems.models import MenuItemFlavor


class MenuItemFlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemFlavor
        fields = ["quantity", "flavor"]


class MenuItemFlavorSerializerReadOnly(ReadOnlyModelSerializer):
    flavor = FlavorSerializerReadOnly()

    class Meta:
        model = MenuItemFlavor
        fields = [
            "quantity",
            "flavor",
        ]
