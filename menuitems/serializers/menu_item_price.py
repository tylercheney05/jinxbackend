from rest_framework import serializers

from menuitems.models import MenuItemPrice


class MenuItemPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItemPrice
        fields = ["id", "price"]
        read_only_fields = ["id"]
